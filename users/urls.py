from django.urls import path
from .views import RegisterView, VerifyOTPView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-user-otp'),
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
]