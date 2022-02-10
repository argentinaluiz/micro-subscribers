from functools import update_wrapper
from django.contrib.admin import AdminSite as DjangoAdminSite
from django.urls.base import reverse
from django.urls.conf import path
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from .views import AdminLogin, AdminLogout


class AdminSite(DjangoAdminSite):
    site_header = "CodeFlix Assinantes"
    site_title = "CodeFlix Assinantes Admin"
    index_title = "Bem-vindo ao CodeFlix Assinantes Admin"

    # def get_urls(self):
    #     url_patterns = super().get_urls()
    #     return [
    #         path('login/', AdminLogin.as_view()),
    #         path('logout/', AdminLogout.as_view())
    #     ] + url_patterns 
    
    def login(self, request):
        return AdminLogin.as_view()(request)
    
    def logout(self, request):
        return AdminLogout.as_view()(request)

    # def admin_view(self, view, cacheable=False):
    #     """
    #     Decorator to create an admin view attached to this ``AdminSite``. This
    #     wraps the view and provides permission checking by calling
    #     ``self.has_permission``.

    #     You'll want to use this from within ``AdminSite.get_urls()``:

    #         class MyAdminSite(AdminSite):

    #             def get_urls(self):
    #                 from django.urls import path

    #                 urls = super().get_urls()
    #                 urls += [
    #                     path('my_view/', self.admin_view(some_view))
    #                 ]
    #                 return urls

    #     By default, admin_views are marked non-cacheable using the
    #     ``never_cache`` decorator. If the view can be safely cached, set
    #     cacheable=True.
    #     """
    #     def inner(request, *args, **kwargs):
    #         if not request.user.is_authenticated: 
    #             from django.contrib.auth.views import redirect_to_login
    #             return redirect_to_login(
    #                 request.get_full_path(),
    #                 reverse('admin:login', current_app=self.name)
    #             )
    #         if not self.has_permission(request):
    #             raise PermissionDenied()
    #         return view(request, *args, **kwargs)
    #     if not cacheable:
    #         inner = never_cache(inner)
    #     # We add csrf_protect here so this function can be used as a utility
    #     # function for any view, without having to repeat 'csrf_protect'.
    #     if not getattr(view, 'csrf_exempt', False):
    #         inner = csrf_protect(inner)
    #     return update_wrapper(inner, view)

    # def has_permission(self, request):
    #     if 'oidc_payload' not in request.session:
    #         return False
    #     payload = request.session['oidc_payload']
    #     print(payload)
    #     resource_access = payload.get('resource_access', {})
    #     real_management = resource_access.get('realm-management')
    #     has_role_subcriber_admin = 'subscribers-admin' in resource_access.get('micro-subscribers', {}).get('roles', [])
    #     """
    #     Return True if the given HttpRequest has permission to view
    #     *at least one* page in the admin site.
    #     """
    #     return request.user.is_active and real_management or has_role_subcriber_admin


admin_site = AdminSite(name='admin_site')