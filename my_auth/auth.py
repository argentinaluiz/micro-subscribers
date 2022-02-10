from base64 import b64decode
from my_auth.models import ResourceAccess
from django.urls.base import reverse
from django.utils.encoding import force_bytes, smart_text
from mozilla_django_oidc.auth import OIDCAuthenticationBackend as DjangoOIDCAuthenticationBackend
import json
from josepy.jws import JWS
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import logging
from django.db import transaction

from mozilla_django_oidc.utils import absolutify

LOGGER = logging.getLogger(__name__)


class OIDCAuthenticationBackend(DjangoOIDCAuthenticationBackend):

    @transaction.atomic
    def create_user(self, claims, payload):
        from my_auth.models import ResourceAccess, Group
        id = claims.get('sub')
        first_name, *last_name = claims.get('name').split()
        email = claims.get('email')
        username = email

        data = {
            'id': id,
            'first_name': first_name,
            'last_name': next(iter(last_name), None),
            'username': username,
            'email': email,
            'is_staff': True,
            'resource_access': payload['resource_access']
        }

        
        resource_access = ResourceAccess(payload['resource_access'])
        if(resource_access.has_client('realm-management')):
            data['is_superuser'] = True

        user = self.UserModel.objects.create_user(**data)
        Group.objects.add_with_user(user, resource_access.get_client_roles('micro-subscribers'))
        return user


    def get_or_create_user(self, access_token, id_token, payload):
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""

        user_info = self.get_userinfo(access_token, id_token, payload)

        email = user_info.get('email')

        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = 'Claims verification failed'
            raise SuspiciousOperation(msg)

        # email based filtering
        users = self.filter_users_by_claims(user_info)

        if len(users) == 1:
            return self.update_user(users[0], user_info, self._get_payload(access_token))
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = 'Multiple users returned'
            raise SuspiciousOperation(msg)
        elif self.get_settings('OIDC_CREATE_USER', True):
            user = self.create_user(user_info, self._get_payload(access_token))
            return user
        else:
            LOGGER.debug('Login failed: No user with email %s found, and '
                         'OIDC_CREATE_USER is False', email)
            return None

    def _get_payload(self, token):
        return json.loads(JWS.from_compact(force_bytes(token)).payload)

    def update_user(self, user, claims, payload):
        user.resource_access = payload['resource_access']
        resource_access = ResourceAccess(payload['resource_access'])
        user.is_superuser = resource_access.has_client('realm-management')
        print(vars(user))
        user.save()
        return user

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""

        self.request = request
        if not self.request:
            return None

        state = self.request.GET.get('state')
        code = self.request.GET.get('code')
        nonce = kwargs.pop('nonce', None)

        if not code or not state:
            return None

        reverse_url = self.get_settings('OIDC_AUTHENTICATION_CALLBACK_URL',
                                        'oidc_authentication_callback')

        token_payload = {
            'client_id': self.OIDC_RP_CLIENT_ID,
            'client_secret': self.OIDC_RP_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': absolutify(
                self.request,
                reverse(reverse_url)
            ),
        }

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get('id_token')
        access_token = token_info.get('access_token')

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)
        self.validate_access_token(access_token=access_token)

        if payload:
            self.store_tokens(access_token, id_token)
            try:
                return self.get_or_create_user(access_token, id_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.warning('failed to get or create user: %s', exc)
                return None

        return None

    def validate_access_token(self, access_token):
        payload = self._get_payload(access_token)
        resource_access = ResourceAccess(payload['resource_access'])
        if(not resource_access.has_client('realm-management') and not resource_access.has_client('micro-subscribers')):
            raise PermissionDenied(
                'User not have realm-management client or subscribers-admin role')
    # def _get_user_permissions(self, user_obj):
    #     print('aqui teste')
    #     return user_obj.user_permissions.all()

    # def get_all_permissions(self, user_obj, obj=None):
    #     if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
    #         return set()
    #     if not hasattr(user_obj, '_perm_cache'):
    #         user_obj._perm_cache = super().get_all_permissions(user_obj)
    #     return user_obj._perm_cache

    # def has_perm(self, user_obj, perm, obj=None):
    #     print(perm)
    #     return user_obj.is_active and super().has_perm(user_obj, perm, obj=obj)

    # def has_module_perms(self, user_obj, app_label):
    #     """
    #     Return True if user_obj has any permissions in the given app_label.
    #     """
    #     print(app_label)
    #     return user_obj.is_active and any(
    #         perm[:perm.index('.')] == app_label
    #         for perm in self.get_all_permissions(user_obj)
    #     )
