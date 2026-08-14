from django.urls import path

from .views import (
    VillageAssessmentExportAPIView,
    VillageAssessmentImportListCreateAPIView,
    VillageAssessmentImportRetrieveUpdateDestroyAPIView,
    VillageAssessmentListCreateAPIView,
    VillageAssessmentRetrieveUpdateDestroyAPIView,
    VillageAssessmentReverifyAPIView,
)

urlpatterns = [
    path(
        "village-assessments/",
        VillageAssessmentListCreateAPIView.as_view(),
        name="village-assessment-list-create",
    ),
    path(
        "village-assessments/export/",
        VillageAssessmentExportAPIView.as_view(),
        name="village-assessment-export",
    ),
    path(
        "village-assessments/<int:pk>/",
        VillageAssessmentRetrieveUpdateDestroyAPIView.as_view(),
        name="village-assessment-detail",
    ),
    path(
        "village-assessments/<int:pk>/reverify/",
        VillageAssessmentReverifyAPIView.as_view(),
        name="village-assessment-reverify",
    ),
    path(
        "village-assessment-imports/",
        VillageAssessmentImportListCreateAPIView.as_view(),
        name="village-assessment-import-list-create",
    ),
    path(
        "village-assessment-imports/<int:pk>/",
        VillageAssessmentImportRetrieveUpdateDestroyAPIView.as_view(),
        name="village-assessment-import-detail",
    ),
]
