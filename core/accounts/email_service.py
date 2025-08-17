import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from celery import shared_task
from .messages import REGISTRATION_MESSAGES

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending various types of emails"""

    @staticmethod
    def get_verification_url(token):
        """Generate email verification URL"""
        return f"{settings.FRONTEND_URL}/verify-email?token={token}"

    @staticmethod
    def get_password_reset_url(token):
        """Generate password reset URL"""
        return f"{settings.FRONTEND_URL}/reset-password?token={token}"

    @staticmethod
    def send_email(subject, template_name, context, recipient_email, from_email=None):
        """Send HTML email with fallback to text"""
        try:
            if from_email is None:
                from_email = settings.DEFAULT_FROM_EMAIL

            # Render HTML template
            html_content = render_to_string(f'emails/{template_name}.html', context)

            # Create text version
            text_content = strip_tags(html_content)

            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[recipient_email]
            )

            # Attach HTML version
            email.attach_alternative(html_content, "text/html")

            # Send email
            email.send()

            logger.info(f"Email sent successfully to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False


@shared_task
def send_verification_email_task(user_id, token):
    """Celery task to send verification email"""
    from core.models import User

    try:
        user = User.objects.get(id=user_id)

        context = {
            'user': user,
            'verification_url': EmailService.get_verification_url(token),
            'site_name': 'ClassDojo Nursery',
            'frontend_url': settings.FRONTEND_URL,
        }

        success = EmailService.send_email(
            subject=REGISTRATION_MESSAGES['email_verification_subject'],
            template_name='email_verification',
            context=context,
            recipient_email=user.email
        )

        if success:
            logger.info(f"Verification email sent to user {user.email}")
        else:
            logger.error(f"Failed to send verification email to user {user.email}")

        return success

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False


@shared_task
def send_welcome_email_task(user_id):
    """Celery task to send welcome email after verification"""
    from core.models import User

    try:
        user = User.objects.get(id=user_id)

        context = {
            'user': user,
            'site_name': 'ClassDojo Nursery',
            'frontend_url': settings.FRONTEND_URL,
            'login_url': f"{settings.FRONTEND_URL}/login",
        }

        success = EmailService.send_email(
            subject=REGISTRATION_MESSAGES['welcome_subject'],
            template_name='welcome',
            context=context,
            recipient_email=user.email
        )

        if success:
            logger.info(f"Welcome email sent to user {user.email}")
        else:
            logger.error(f"Failed to send welcome email to user {user.email}")

        return success

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False


@shared_task
def send_password_reset_email_task(user_id, token):
    """Celery task to send password reset email"""
    from core.models import User

    try:
        user = User.objects.get(id=user_id)

        context = {
            'user': user,
            'reset_url': EmailService.get_password_reset_url(token),
            'site_name': 'ClassDojo Nursery',
            'frontend_url': settings.FRONTEND_URL,
        }

        success = EmailService.send_email(
            subject=REGISTRATION_MESSAGES['password_reset_subject'],
            template_name='password_reset',
            context=context,
            recipient_email=user.email
        )

        if success:
            logger.info(f"Password reset email sent to user {user.email}")
        else:
            logger.error(f"Failed to send password reset email to user {user.email}")

        return success

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False


def send_verification_email(user):
    """Send verification email (sync or async based on settings)"""
    token = user.generate_email_verification_token()

    try:
        if hasattr(settings, 'CELERY_BROKER_URL') and settings.CELERY_BROKER_URL:
            # Send async with Celery
            send_verification_email_task.delay(user.id, str(token))
        else:
            # Send synchronously
            send_verification_email_task(user.id, str(token))
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        # Fallback to synchronous sending
        send_verification_email_task(user.id, str(token))


def send_welcome_email(user):
    """Send welcome email (sync or async based on settings)"""
    try:
        if hasattr(settings, 'CELERY_BROKER_URL') and settings.CELERY_BROKER_URL:
            # Send async with Celery
            send_welcome_email_task.delay(user.id)
        else:
            # Send synchronously
            send_welcome_email_task(user.id)
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        # Fallback to synchronous sending
        send_welcome_email_task(user.id)