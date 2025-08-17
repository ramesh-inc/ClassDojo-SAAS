from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.models import User
from .serializers import (
    ParentRegistrationSerializer,
    AdminRegistrationSerializer,
    TeacherRegistrationSerializer,
    EmailVerificationSerializer,
    ResendVerificationSerializer,
    UserProfileSerializer
)
from .email_service import send_verification_email, send_welcome_email
from .messages import REGISTRATION_MESSAGES, AUTH_MESSAGES
from .permissions import IsAdminUser, IsSuperAdminUser
import logging

logger = logging.getLogger(__name__)


class ParentRegistrationView(APIView):
    """
    Parent registration endpoint
    Open to public - parents can self-register
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new parent account",
        request_body=ParentRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Registration successful",
                examples={
                    "application/json": {
                        "message": "Account created successfully! Please check your email to verify your account.",
                        "user_id": 123,
                        "email": "parent@example.com"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation errors",
                examples={
                    "application/json": {
                        "email": ["An account with this email address already exists."],
                        "confirm_password": ["Passwords do not match."]
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Register a new parent"""
        serializer = ParentRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()

                    # Send verification email
                    send_verification_email(user)

                    logger.info(f"Parent registration successful: {user.email}")

                    return Response({
                        'message': REGISTRATION_MESSAGES['registration_success'],
                        'user_id': user.id,
                        'email': user.email
                    }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Parent registration failed: {str(e)}")
                return Response({
                    'error': 'Registration failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    """
    Admin registration endpoint
    Only accessible by super admins
    """
    permission_classes = [IsSuperAdminUser]

    @swagger_auto_schema(
        operation_description="Register a new admin account (Super Admin only)",
        request_body=AdminRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Admin registration successful",
                examples={
                    "application/json": {
                        "message": "Admin account created successfully.",
                        "user_id": 124,
                        "email": "admin@example.com"
                    }
                }
            ),
            403: openapi.Response(description="Permission denied"),
            400: openapi.Response(description="Validation errors")
        },
        tags=['Admin Management']
    )
    def post(self, request):
        """Register a new admin (Super Admin only)"""
        serializer = AdminRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()

                    logger.info(f"Admin registration successful: {user.email}")

                    return Response({
                        'message': 'Admin account created successfully.',
                        'user_id': user.id,
                        'email': user.email
                    }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Admin registration failed: {str(e)}")
                return Response({
                    'error': 'Registration failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegistrationView(APIView):
    """
    Teacher registration endpoint
    Only accessible by admins
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Register a new teacher account (Admin only)",
        request_body=TeacherRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Teacher registration successful",
                examples={
                    "application/json": {
                        "message": "Teacher account created successfully.",
                        "user_id": 125,
                        "email": "teacher@example.com",
                        "employee_id": "TCH001"
                    }
                }
            ),
            403: openapi.Response(description="Permission denied"),
            400: openapi.Response(description="Validation errors")
        },
        tags=['Admin Management']
    )
    def post(self, request):
        """Register a new teacher (Admin only)"""
        serializer = TeacherRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()

                    # Send welcome email to teacher
                    send_welcome_email(user)

                    logger.info(f"Teacher registration successful: {user.email}")

                    return Response({
                        'message': 'Teacher account created successfully.',
                        'user_id': user.id,
                        'email': user.email,
                        'employee_id': user.teacher_profile.employee_id
                    }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Teacher registration failed: {str(e)}")
                return Response({
                    'error': 'Registration failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    Email verification endpoint
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Verify email address using verification token",
        request_body=EmailVerificationSerializer,
        responses={
            200: openapi.Response(
                description="Email verified successfully",
                examples={
                    "application/json": {
                        "message": "Email verified successfully! Your account is now active.",
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid or expired token",
                examples={
                    "application/json": {
                        "token": ["Invalid verification token."]
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Verify email address"""
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                token = serializer.validated_data['token']

                with transaction.atomic():
                    user = User.objects.get(
                        email_verification_token=token,
                        email_verified=False
                    )

                    # Verify email and activate account
                    user.email_verified = True
                    user.is_active = True
                    user.email_verification_token = None
                    user.email_verification_sent_at = None
                    user.save()

                    # Send welcome email
                    send_welcome_email(user)

                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)

                    logger.info(f"Email verification successful: {user.email}")

                    return Response({
                        'message': REGISTRATION_MESSAGES['email_verification_success'],
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user': UserProfileSerializer(user).data
                    }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                pass
            except Exception as e:
                logger.error(f"Email verification failed: {str(e)}")
                return Response({
                    'error': 'Verification failed. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    """
    Resend email verification
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Resend email verification",
        request_body=ResendVerificationSerializer,
        responses={
            200: openapi.Response(
                description="Verification email sent",
                examples={
                    "application/json": {
                        "message": "Verification email sent successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Email not found or already verified",
                examples={
                    "application/json": {
                        "email": ["Email not found or already verified."]
                    }
                }
            ),
            429: openapi.Response(
                description="Rate limited - too many requests",
                examples={
                    "application/json": {
                        "error": "Please wait before requesting another verification email."
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Resend verification email"""
        serializer = ResendVerificationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                user = User.objects.get(email=email, email_verified=False)

                # Check rate limiting (prevent spam)
                if (user.email_verification_sent_at and
                        timezone.now() < user.email_verification_sent_at + timezone.timedelta(minutes=1)):
                    return Response({
                        'error': 'Please wait before requesting another verification email.'
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)

                # Send new verification email
                send_verification_email(user)

                logger.info(f"Verification email resent: {user.email}")

                return Response({
                    'message': REGISTRATION_MESSAGES['verification_email_sent']
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                pass
            except Exception as e:
                logger.error(f"Resend verification failed: {str(e)}")
                return Response({
                    'error': 'Failed to send verification email. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view with additional validation
    """

    @swagger_auto_schema(
        operation_description="Obtain JWT access and refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "user_type": "parent"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials or account issues",
                examples={
                    "application/json": {
                        "error": "Please verify your email before logging in."
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        """Login with email and password"""
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'error': 'Email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if user exists
            user = User.objects.get(email=email)

            # Check if email is verified
            if not user.email_verified:
                return Response({
                    'error': AUTH_MESSAGES['account_not_verified']
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if account is active
            if not user.is_active:
                return Response({
                    'error': AUTH_MESSAGES['account_inactive']
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'error': AUTH_MESSAGES['invalid_credentials']
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            logger.info(f"User login successful: {user.email}")

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Failed login attempt for: {email}")
            return Response({
                'error': AUTH_MESSAGES['invalid_credentials']
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Get user profile information
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get current user profile",
        responses={
            200: openapi.Response(
                description="User profile data",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "user@example.com",
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "user_type": "parent",
                        "phone_number": "+94771234567",
                        "preferred_language": "en",
                        "email_verified": True,
                        "is_active": True
                    }
                }
            )
        },
        tags=['User Profile']
    )
    def get(self, request):
        """Get current user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Check API health status",
    responses={
        200: openapi.Response(
            description="API is healthy",
            examples={
                "application/json": {
                    "status": "healthy",
                    "timestamp": "2025-01-20T10:30:00Z",
                    "version": "1.0.0"
                }
            }
        )
    },
    tags=['Health Check']
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)