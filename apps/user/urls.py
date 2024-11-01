from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
) 

from .api_endpoints import *

app_name = 'user'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='user-register'),
    path('verification/email/<str:url>/', VerificationEmailApi.as_view(), name='verification-email'),
    path('login/', LoginApi.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh')

]
