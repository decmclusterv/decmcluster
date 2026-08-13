from django.urls import path

from .views import (
    CommunityLevelDamageAssessmentFormDetailView,
    CommunityLevelDamageAssessmentFormListCreateView,
    DamageAssessmentFormCommunityV2DetailView,
    DamageAssessmentFormCommunityV2ListCreateView,
    DisplacementProfilePhoneSurveyDetailView,
    DisplacementProfilePhoneSurveyListCreateView,
    DisplacementTrackingMatrixFormDetailView,
    DisplacementTrackingMatrixFormListCreateView,
    DurableSolutionRelocationSurveyDetailView,
    DurableSolutionRelocationSurveyListCreateView,
    RapidAssessmentFormAreaCouncilDetailView,
    RapidAssessmentFormAreaCouncilListCreateView,
    ServiceMonitoringTool2026DetailView,
    ServiceMonitoringTool2026ListCreateView,
)

urlpatterns = [
    # Durable Solution & Relocation Survey
    path(
        "durable-solution-relocation-survey/",
        DurableSolutionRelocationSurveyListCreateView.as_view(),
        name="durable-solution-relocation-survey-list",
    ),
    path(
        "durable-solution-relocation-survey/<int:pk>/",
        DurableSolutionRelocationSurveyDetailView.as_view(),
        name="durable-solution-relocation-survey-detail",
    ),
    # Service Monitoring Tool 2026
    path(
        "service-monitoring-tool-2026/",
        ServiceMonitoringTool2026ListCreateView.as_view(),
        name="service-monitoring-tool-2026-list",
    ),
    path(
        "service-monitoring-tool-2026/<int:pk>/",
        ServiceMonitoringTool2026DetailView.as_view(),
        name="service-monitoring-tool-2026-detail",
    ),
    # Displacement Tracking Matrix Form
    path(
        "displacement-tracking-matrix-form/",
        DisplacementTrackingMatrixFormListCreateView.as_view(),
        name="displacement-tracking-matrix-form-list",
    ),
    path(
        "displacement-tracking-matrix-form/<int:pk>/",
        DisplacementTrackingMatrixFormDetailView.as_view(),
        name="displacement-tracking-matrix-form-detail",
    ),
    # Rapid Assessment Form (Area Council)
    path(
        "rapid-assessment-form-area-council/",
        RapidAssessmentFormAreaCouncilListCreateView.as_view(),
        name="rapid-assessment-form-area-council-list",
    ),
    path(
        "rapid-assessment-form-area-council/<int:pk>/",
        RapidAssessmentFormAreaCouncilDetailView.as_view(),
        name="rapid-assessment-form-area-council-detail",
    ),
    # Community Level Damage Assessment Form
    path(
        "community-level-damage-assessment-form/",
        CommunityLevelDamageAssessmentFormListCreateView.as_view(),
        name="community-level-damage-assessment-form-list",
    ),
    path(
        "community-level-damage-assessment-form/<int:pk>/",
        CommunityLevelDamageAssessmentFormDetailView.as_view(),
        name="community-level-damage-assessment-form-detail",
    ),
    # Displacement Profile - Phone Survey
    path(
        "displacement-profile-phone-survey/",
        DisplacementProfilePhoneSurveyListCreateView.as_view(),
        name="displacement-profile-phone-survey-list",
    ),
    path(
        "displacement-profile-phone-survey/<int:pk>/",
        DisplacementProfilePhoneSurveyDetailView.as_view(),
        name="displacement-profile-phone-survey-detail",
    ),
    # Damage Assessment Form (Community V2)
    path(
        "damage-assessment-form-community-v2/",
        DamageAssessmentFormCommunityV2ListCreateView.as_view(),
        name="damage-assessment-form-community-v2-list",
    ),
    path(
        "damage-assessment-form-community-v2/<int:pk>/",
        DamageAssessmentFormCommunityV2DetailView.as_view(),
        name="damage-assessment-form-community-v2-detail",
    ),
]
