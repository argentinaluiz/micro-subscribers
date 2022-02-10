from django.shortcuts import render
from django.urls.base import reverse
from mozilla_django_oidc.views import OIDCLogoutView as DjangoOIDCLogoutView, OIDCAuthenticationRequestView, OIDCAuthenticationCallbackView as DjangoOIDCAuthenticationCallbackView
# Create your views here.
from django.conf import settings

class OIDCAuthenticationCallbackView(DjangoOIDCAuthenticationCallbackView):
    pass


class OIDCLoginView(OIDCAuthenticationRequestView):
    pass


class OIDCLogoutView(DjangoOIDCLogoutView):
    """Logout helper view"""

    def get(self, request):
        return self.post(request)

def after_logout(request):
    return settings.OIDC_AUTH_URI + '/logout' + '?redirect_uri=' + request.build_absolute_uri(reverse('auth:login'))