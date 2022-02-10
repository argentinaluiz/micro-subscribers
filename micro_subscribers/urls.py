"""micro_subscribers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.urls.base import reverse
from django.urls.conf import include
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from my_admin.admin import admin_site
from django.conf.urls.static import static
from django.conf import settings

def home(request):
    print(request.user.is_authenticated)
    return HttpResponse('Olá mundo')


@login_required
def dashboard(request):
    print(request.session['oidc_payload'])
    return HttpResponse('Dashboard')


urlpatterns = [
    #path('admin/login/', CustomLogin.as_view()),
    #path('admin/logout/', CustomLogout.as_view()),
    path('admin/', admin_site.urls),
    path('auth/', include('my_auth.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    #path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('', home),
    path('dashboard/', dashboard),
]

if settings.APP_ENV:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)