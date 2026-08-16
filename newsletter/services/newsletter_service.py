import logging
from django.conf import settings
from newsletter.models import Newsletter
from decmcluster.services.email_service import send_bcc_html_email

logger = logging.getLogger(__name__)


def subscribe_email(email: str) -> Newsletter:
    """
    Subscribes an email to the newsletter.
    If the email already exists and was unsubscribed, it updates the status to subscribed.
    If it is a new email, it creates a new subscription record.
    """
    newsletter, created = Newsletter.objects.get_or_create(
        email=email,
        defaults={"is_subscribed": True}
    )
    if not created and not newsletter.is_subscribed:
        newsletter.is_subscribed = True
        newsletter.save(update_fields=["is_subscribed"])
    return newsletter


def unsubscribe_email(email: str) -> bool:
    """
    Unsubscribes an email from the newsletter.
    Returns True if the email was found and unsubscribed, False otherwise.
    """
    try:
        newsletter = Newsletter.objects.get(email=email)
        if newsletter.is_subscribed:
            newsletter.is_subscribed = False
            newsletter.save(update_fields=["is_subscribed"])
            return True
    except Newsletter.DoesNotExist:
        pass
    return False


def send_custom_newsletter_emails(subject: str, body: str, emails: list = None) -> dict:
    """
    Sends a custom email with a given subject and body to newsletter subscribers in a single email using BCC.
    If emails is provided, sends to those emails (subscribing/reactivating them if not already active).
    If emails is not provided, sends to all active newsletter subscribers.
    Returns a dict with count of successful and failed email sends.
    """
    if emails is not None and len(emails) > 0:
        target_emails = []
        for email in emails:
            email = email.lower().strip()
            # Automatically subscribe if not present or inactive
            subscribe_email(email)
            target_emails.append(email)
    else:
        target_emails = list(
            Newsletter.objects.filter(is_subscribed=True).values_list("email", flat=True)
        )

    if not target_emails:
        return {"success_count": 0, "failure_count": 0}

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "info@decmcluster.org")
    context = {"body": body}

    success = send_bcc_html_email(
        subject=subject,
        to_email=from_email,
        bcc_emails=target_emails,
        template_name="emails/newsletter_custom.html",
        context=context,
    )

    if success:
        return {"success_count": len(target_emails), "failure_count": 0}
    else:
        return {"success_count": 0, "failure_count": len(target_emails)}


def update_subscription_status(email: str, is_subscribed: bool) -> Newsletter:
    """
    Updates the subscription status of a newsletter email.
    If the email already exists, updates the status.
    If the email does not exist, creates a new subscription record with the given status.
    """
    email = email.lower().strip()
    newsletter, created = Newsletter.objects.get_or_create(
        email=email,
        defaults={"is_subscribed": is_subscribed}
    )
    if not created and newsletter.is_subscribed != is_subscribed:
        newsletter.is_subscribed = is_subscribed
        newsletter.save(update_fields=["is_subscribed"])
    return newsletter


