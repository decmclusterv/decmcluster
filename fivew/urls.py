from django.urls import path

from .views import (
    FiveWActivityExportAPIView,
    FiveWActivityListCreateAPIView,
    FiveWActivityRetrieveUpdateDestroyAPIView,
    FiveWImportListCreateAPIView,
    FiveWImportRetrieveUpdateDestroyAPIView,
    FiveWActivityReverifyAPIView,
)

urlpatterns = [
    path(
        "fivew/activities/",
        FiveWActivityListCreateAPIView.as_view(),
        name="fivew-activity-list-create",
    ),
    path(
        "fivew/activities/export/",
        FiveWActivityExportAPIView.as_view(),
        name="fivew-activity-export",
    ),
    path(
        "fivew/activities/<int:pk>/",
        FiveWActivityRetrieveUpdateDestroyAPIView.as_view(),
        name="fivew-activity-detail",
    ),
    path(
        "fivew/activities/<int:pk>/reverify/",
        FiveWActivityReverifyAPIView.as_view(),
        name="fivew-activity-reverify",
    ),
    path(
        "fivew/imports/",
        FiveWImportListCreateAPIView.as_view(),
        name="fivew-import-list-create",
    ),
    path(
        "fivew/imports/<int:pk>/",
        FiveWImportRetrieveUpdateDestroyAPIView.as_view(),
        name="fivew-import-detail",
    ),
]
