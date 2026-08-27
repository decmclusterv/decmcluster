from django.db.models import QuerySet

from cluster_contact.models import ClusterContact


def get_cluster_contacts() -> QuerySet[ClusterContact]:
    """Retrieve all cluster contacts ordered by latest created_at."""
    return ClusterContact.objects.all().order_by("-created_at")
