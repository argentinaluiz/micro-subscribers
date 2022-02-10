from django.urls import path
from django.shortcuts import render

def test(request):
    return render(request, 'subscriptions/index.html')

app_name = "subscriptions"

urlpatterns = [
    path('', test, name='test'),
]
