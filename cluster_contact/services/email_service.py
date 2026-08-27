import logging
from typing import Dict, List, Optional

from django.conf import settings

from cluster_contact.models import ClusterContact
from decmcluster.services.email_service import send_bcc_html_email

logger = logging.getLogger(__name__)


def send_cluster_contact_emails(
    subject: str, body: str, emails: Optional[List[str]] = None
) -> Dict[str, int]:
    """
    Sends custom emails with given subject and rich text body to Cluster Contact emails using BCC.
    If emails is provided, sends to those specified emails.
    If emails is None or empty, sends to all emails registered in ClusterContact table.
    """
    if emails is not None and len(emails) > 0:
        target_emails = [email.lower().strip() for email in emails if email]
    else:
        target_emails = list(
            ClusterContact.objects.values_list("email", flat=True).distinct()
        )

    if not target_emails:
        return {"success_count": 0, "failure_count": 0}

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "info@decmcluster.org")
    context = {"body": body}

    success = send_bcc_html_email(
        subject=subject,
        to_email=from_email,
        bcc_emails=target_emails,
        template_name="emails/cluster_contact_email.html",
        context=context,
    )

    if success:
        return {"success_count": len(target_emails), "failure_count": 0}
    else:
        return {"success_count": 0, "failure_count": len(target_emails)}
