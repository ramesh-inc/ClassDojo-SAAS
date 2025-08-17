from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ParentRegistrationView,
    AdminRegistrationView,
    TeacherRegistrationView,
    EmailVerificationView,
    ResendVerificationView,
    CustomTokenObtainPairView,
    UserProfileView,
    health_check,
)

app_name = 'accounts_auth'  # Changed to unique namespace

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),

    # Registration endpoints
    path('register/parent/', ParentRegistrationView.as_view(), name='parent_register'),
    path('register/admin/', AdminRegistrationView.as_view(), name='admin_register'),
    path('register/teacher/', TeacherRegistrationView.as_view(), name='teacher_register'),

    # Email verification
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend_verification'),

    # Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]