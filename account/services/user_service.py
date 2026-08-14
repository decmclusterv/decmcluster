import logging

from django.conf import settings

from account.services.verification_service import generate_verification_token
from decmcluster.services.email_service import send_html_email

logger = logging.getLogger(__name__)


def send_verification_email(user) -> bool:
    """
    Generates a verification token and sends verification email to the user.
    """
    token = generate_verification_token(user)

    # Resolve frontend url
    frontend_url = getattr(settings, "ADMIN_URL", "http://localhost:3000")
    if not frontend_url:
        frontend_url = "http://localhost:3000"

    if not frontend_url.endswith("/"):
        frontend_url += "/"

    # The link will redirect the user to the frontend verification route
    verification_url = f"{frontend_url}verify-email?token={token}"

    subject = "Verify Your Email - DECM Cluster"
    context = {
        "user": user,
        "verification_url": verification_url,
    }

    logger.info(f"Sending verification email to {user.email}")

    return send_html_email(
        subject=subject,
        to_email=user.email,
        template_name="emails/user_verification.html",
        context=context,
    )


def change_user_password(user, new_password) -> None:
    """
    Sets the new password for the user and saves it.
    """
    user.set_password(new_password)
    user.save()
    logger.info(f"Password changed successfully for user: {user.email}")

