from django.db.models import QuerySet
from newsletter.models import Newsletter


def get_newsletter_subscribers() -> QuerySet[Newsletter]:
    """
    Retrieve all newsletter subscribers, ordered by latest subscription date first.
    """
    return Newsletter.objects.all().order_by("-created_at")
