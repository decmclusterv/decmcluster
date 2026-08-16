import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_html_email(subject, to_email, template_name, context):
    """
    Renders an HTML template and sends it using smtplib via Zoho Mail SMTP.
    """
    smtp_server = getattr(settings, "EMAIL_HOST", "smtp.zohocloud.ca")
    smtp_port = int(getattr(settings, "EMAIL_PORT", 587))
    email_user = getattr(settings, "EMAIL_HOST_USER", None)
    app_password = getattr(settings, "EMAIL_HOST_PASSWORD", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", email_user)

    if not email_user or not app_password:
        logger.error(
            "EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not configured in settings."
        )
        return False

    if not from_email:
        from_email = email_user

    recipient_list = [to_email] if isinstance(to_email, str) else list(to_email)

    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
    except Exception as e:
        logger.exception(f"Error rendering template {template_name}: {e}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(recipient_list)

        part_text = MIMEText(text_content, "plain")
        part_html = MIMEText(html_content, "html")

        msg.attach(part_text)
        msg.attach(part_html)

        use_ssl = getattr(settings, "EMAIL_USE_SSL", False)

        if use_ssl or smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(email_user, app_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_user, app_password)
                server.send_message(msg)

        logger.info(
            f"Email sent successfully via Zoho SMTP. Subject: {subject}. To: {recipient_list}"
        )
        return True
    except Exception as e:
        logger.exception(f"Error sending email via Zoho SMTP: {e}")
        return False


def send_batch_html_emails(email_data_list: list) -> dict:
    """
    Sends multiple HTML emails in a batch using a single SMTP connection.
    email_data_list should be a list of dicts:
    [
        {
            "subject": str,
            "to_email": str or list,
            "template_name": str,
            "context": dict
        },
        ...
    ]
    Returns a dict with success_count and failure_count.
    """
    smtp_server = getattr(settings, "EMAIL_HOST", "smtp.zohocloud.ca")
    smtp_port = int(getattr(settings, "EMAIL_PORT", 587))
    email_user = getattr(settings, "EMAIL_HOST_USER", None)
    app_password = getattr(settings, "EMAIL_HOST_PASSWORD", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", email_user)

    if not email_user or not app_password:
        logger.error(
            "EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not configured in settings."
        )
        return {"success_count": 0, "failure_count": len(email_data_list)}

    if not from_email:
        from_email = email_user

    use_ssl = getattr(settings, "EMAIL_USE_SSL", False)
    success_count = 0
    failure_count = 0

    def send_messages(server):
        nonlocal success_count, failure_count
        for email_data in email_data_list:
            subject = email_data.get("subject")
            to_email = email_data.get("to_email")
            template_name = email_data.get("template_name")
            context = email_data.get("context", {})

            recipient_list = [to_email] if isinstance(to_email, str) else list(to_email)

            try:
                html_content = render_to_string(template_name, context)
                text_content = strip_tags(html_content)

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = from_email
                msg["To"] = ", ".join(recipient_list)

                part_text = MIMEText(text_content, "plain")
                part_html = MIMEText(html_content, "html")

                msg.attach(part_text)
                msg.attach(part_html)

                server.send_message(msg)
                success_count += 1
                logger.info(
                    f"Email sent successfully in batch. Subject: {subject}. To: {recipient_list}"
                )
            except Exception as e:
                failure_count += 1
                logger.exception(
                    f"Failed to send email in batch to {recipient_list}: {e}"
                )

    try:
        if use_ssl or smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(email_user, app_password)
                send_messages(server)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_user, app_password)
                send_messages(server)
    except Exception as e:
        logger.exception(f"Error in batch SMTP session: {e}")
        # Mark remaining as failed if connection failed
        total_remaining = len(email_data_list) - (success_count + failure_count)
        failure_count += total_remaining

    return {"success_count": success_count, "failure_count": failure_count}


def send_bcc_html_email(
    subject: str,
    to_email: str,
    bcc_emails: list,
    template_name: str,
    context: dict,
) -> bool:
    """
    Sends an HTML email with BCC recipients using smtplib.
    to_email is typically the sender's own email address or a placeholder.
    bcc_emails is a list of strings (BCC recipients).
    """
    smtp_server = getattr(settings, "EMAIL_HOST", "smtp.zohocloud.ca")
    smtp_port = int(getattr(settings, "EMAIL_PORT", 587))
    email_user = getattr(settings, "EMAIL_HOST_USER", None)
    app_password = getattr(settings, "EMAIL_HOST_PASSWORD", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", email_user)

    if not email_user or not app_password:
        logger.error(
            "EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not configured in settings."
        )
        return False

    if not from_email:
        from_email = email_user

    bcc_list = [bcc_emails] if isinstance(bcc_emails, str) else list(bcc_emails)
    if not bcc_list:
        return False

    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
    except Exception as e:
        logger.exception(f"Error rendering template {template_name}: {e}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        part_text = MIMEText(text_content, "plain")
        part_html = MIMEText(html_content, "html")

        msg.attach(part_text)
        msg.attach(part_html)

        use_ssl = getattr(settings, "EMAIL_USE_SSL", False)
        all_recipients = [to_email] + bcc_list

        if use_ssl or smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(email_user, app_password)
                server.sendmail(from_email, all_recipients, msg.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_user, app_password)
                server.sendmail(from_email, all_recipients, msg.as_string())

        logger.info(
            f"BCC email sent successfully via SMTP. Subject: {subject}. To: {to_email}. BCC count: {len(bcc_list)}"
        )
        return True
    except Exception as e:
        logger.exception(f"Error sending BCC email via SMTP: {e}")
        return False


def send_model_verification_email(
    instance, model_name, details, admin_email=None, admin_url=None
):
    """
    Standardized function to send a verification email to the admin for any model creation.
    """
    if not admin_email:
        admin_email = getattr(settings, "ADMIN_EMAIL", None)

    if not admin_email:
        logger.error("ADMIN_EMAIL is not configured in settings.")
        return False

    if not admin_url:
        admin_url = getattr(
            settings, "ADMIN_URL", "https://decmcluster.org/verify-content/"
        )

    subject = f"Verification Required: New {model_name} Created."
    context = {
        "model_name": model_name,
        "instance_name": str(instance),
        "instance_status": instance.status.capitalize(),
        "details": details,
        "admin_url": admin_url,
    }

    return send_html_email(
        subject=subject,
        to_email=admin_email,
        template_name="emails/verification.html",
        context=context,
    )


def send_status_update_email(instance, model_name, new_status, comment=None):
    """
    Sends a notification email to the uploader when a model status changes.
    """
    if not instance.uploaded_by or not instance.uploaded_by.email:
        logger.warning(
            f"No uploader or uploader email found for {model_name} {instance.id}. Skipping email."
        )
        return False

    to_email = instance.uploaded_by.email
    instance_name = str(instance)

    if new_status == "verified":
        subject = f"Verified: Your {model_name} has been verified."
        template_name = "emails/verified.html"
        context = {
            "model_name": model_name,
            "instance_name": instance_name,
        }
    elif new_status == "returned":
        subject = f"Action Required: Your {model_name} was returned."
        template_name = "emails/returned.html"
        base_url = getattr(settings, "ADMIN_URL", "http://192.168.1.80:3000/")
        if not base_url.endswith("/"):
            base_url += "/"

        # Build edit url dynamically based on model name
        model_path = model_name.lower().replace(" ", "-")
        edit_url = f"{base_url}{model_path}/edit/{instance.id}/"

        context = {
            "model_name": model_name,
            "instance_name": instance_name,
            "comment": comment
            or getattr(instance, "comment", "")
            or "No comment provided.",
            "edit_url": edit_url,
        }
    else:
        logger.warning(f"No email flow defined for status: {new_status}")
        return False

    return send_html_email(
        subject=subject,
        to_email=to_email,
        template_name=template_name,
        context=context,
    )

