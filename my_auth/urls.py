from django.urls import path
from .views import OIDCAuthenticationCallbackView, OIDCLoginView, OIDCLogoutView

app_name="auth"

urlpatterns = [
    path('callback/', OIDCAuthenticationCallbackView.as_view(), name='callback'),
    path('login/', OIDCLoginView.as_view(), name='login'),
    path('logout/', OIDCLogoutView.as_view(), name='logout'),
]
