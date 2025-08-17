from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from core.models import User, Parent, Admin, Teacher
from .validators import validate_phone_number, validate_name
from .messages import REGISTRATION_MESSAGES


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Base user registration serializer"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(validators=[validate_name], max_length=150)
    last_name = serializers.CharField(validators=[validate_name], max_length=150)
    phone_number = serializers.CharField(validators=[validate_phone_number], required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'preferred_language', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(REGISTRATION_MESSAGES['email_exists'])
        return value.lower()

    def validate(self, attrs):
        """Cross-field validation"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': REGISTRATION_MESSAGES['passwords_dont_match']
            })
        return attrs

    def create(self, validated_data):
        """Create user with email verification token"""
        validated_data.pop('confirm_password')

        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['email'],  # Use email as username
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                phone_number=validated_data.get('phone_number', ''),
                preferred_language=validated_data.get('preferred_language', 'en'),
                password=validated_data['password'],
                is_active=False,  # Inactive until email verified
            )

            # Generate email verification token
            user.generate_email_verification_token()

            return user


class ParentRegistrationSerializer(UserRegistrationSerializer):
    """Parent registration serializer"""
    occupation = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact = serializers.CharField(
        validators=[validate_phone_number],
        required=False,
        allow_blank=True
    )
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + [
            'occupation', 'emergency_contact', 'address'
        ]

    def create(self, validated_data):
        """Create parent user and profile"""
        # Extract parent-specific fields
        parent_fields = {
            'occupation': validated_data.pop('occupation', ''),
            'emergency_contact': validated_data.pop('emergency_contact', ''),
            'address': validated_data.pop('address', ''),
        }

        with transaction.atomic():
            # Create user
            user = super().create(validated_data)
            user.user_type = 'parent'
            user.save()

            # Create parent profile
            Parent.objects.create(
                user=user,
                **parent_fields
            )

            return user


class AdminRegistrationSerializer(UserRegistrationSerializer):
    """Admin registration serializer (used by super admin)"""
    admin_level = serializers.ChoiceField(choices=Admin.ADMIN_LEVELS, default='admin')
    permissions = serializers.JSONField(required=False, default=dict)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + [
            'admin_level', 'permissions'
        ]

    def create(self, validated_data):
        """Create admin user and profile"""
        # Extract admin-specific fields
        admin_fields = {
            'admin_level': validated_data.pop('admin_level', 'admin'),
            'permissions': validated_data.pop('permissions', {}),
        }

        with transaction.atomic():
            # Create user
            user = super().create(validated_data)
            user.user_type = 'admin'
            user.is_active = True  # Admins are active immediately
            user.email_verified = True  # Skip email verification for admins
            user.save()

            # Create admin profile
            Admin.objects.create(
                user=user,
                **admin_fields
            )

            return user


class TeacherRegistrationSerializer(UserRegistrationSerializer):
    """Teacher registration serializer (used by admin)"""
    employee_id = serializers.CharField(max_length=50)
    qualification = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(min_value=0, default=0)
    hire_date = serializers.DateField(required=False, allow_null=True)

    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + [
            'employee_id', 'qualification', 'experience_years', 'hire_date'
        ]

    def validate_employee_id(self, value):
        """Validate employee ID uniqueness"""
        if Teacher.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError(REGISTRATION_MESSAGES['employee_id_exists'])
        return value

    def create(self, validated_data):
        """Create teacher user and profile"""
        # Extract teacher-specific fields
        teacher_fields = {
            'employee_id': validated_data.pop('employee_id'),
            'qualification': validated_data.pop('qualification', ''),
            'experience_years': validated_data.pop('experience_years', 0),
            'hire_date': validated_data.pop('hire_date', None),
        }

        with transaction.atomic():
            # Create user
            user = super().create(validated_data)
            user.user_type = 'teacher'
            user.is_active = True  # Teachers are active immediately
            user.email_verified = True  # Skip email verification for teachers
            user.save()

            # Create teacher profile
            Teacher.objects.create(
                user=user,
                **teacher_fields
            )

            return user


class EmailVerificationSerializer(serializers.Serializer):
    """Email verification serializer"""
    token = serializers.UUIDField()

    def validate_token(self, value):
        """Validate verification token"""
        try:
            user = User.objects.get(
                email_verification_token=value,
                email_verified=False
            )
            if user.is_email_verification_expired():
                raise serializers.ValidationError(REGISTRATION_MESSAGES['verification_expired'])
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError(REGISTRATION_MESSAGES['invalid_verification_token'])


class ResendVerificationSerializer(serializers.Serializer):
    """Resend email verification serializer"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Validate email exists and not verified"""
        try:
            user = User.objects.get(email=value, email_verified=False)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError(REGISTRATION_MESSAGES['email_not_found_or_verified'])


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for authenticated users"""
    full_name = serializers.SerializerMethodField()
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'preferred_language', 'user_type', 'avatar_url',
            'email_verified', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'email', 'email_verified', 'is_active', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()