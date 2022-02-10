from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import View

# Create your views here.


class AdminLogin(View):
    def get(self, request):
        return HttpResponseRedirect(
            reverse('auth:login') + (
                f"?{request.META['QUERY_STRING']}" if request.META['QUERY_STRING'] else ''
            )
        )


class AdminLogout(View):
    def get(self, request):
        return HttpResponseRedirect(
            reverse('auth:logout') + (
                f"?{request.META['QUERY_STRING']}" if request.META['QUERY_STRING'] else ''
            )
        )
