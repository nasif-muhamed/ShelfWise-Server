from django.urls import path
from .views import RegisterView, VerifyOTPView, AdminUserListView, UserProfileView, \
    AdminUserActionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # auth
    path('register/', RegisterView.as_view(), name='register-user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-user-otp'),
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),

    # users
    path('', AdminUserListView.as_view(), name='users-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-action/<int:pk>/', AdminUserActionView.as_view(), name='admin-user-action'),

]