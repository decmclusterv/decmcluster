from django.urls import path

from .views import (
    ClusterContactDetailAPIView,
    ClusterContactImportAPIView,
    ClusterContactListCreateAPIView,
    SendClusterContactEmailAPIView,
)

urlpatterns = [
    path(
        "cluster-contact/",
        ClusterContactListCreateAPIView.as_view(),
        name="cluster-contact-list-create",
    ),
    path(
        "cluster-contact/import/",
        ClusterContactImportAPIView.as_view(),
        name="cluster-contact-import",
    ),
    path(
        "cluster-contact/send-email/",
        SendClusterContactEmailAPIView.as_view(),
        name="cluster-contact-send-email",
    ),
    path(
        "cluster-contact/<int:pk>/",
        ClusterContactDetailAPIView.as_view(),
        name="cluster-contact-detail",
    ),
]
