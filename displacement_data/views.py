from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .filters import (
    CommunityLevelDamageAssessmentFormFilter,
    DamageAssessmentFormCommunityV2Filter,
    DisplacementProfilePhoneSurveyFilter,
    DisplacementTrackingMatrixFormFilter,
    DurableSolutionRelocationSurveyFilter,
    RapidAssessmentFormAreaCouncilFilter,
    ServiceMonitoringTool2026Filter,
)
from .models import (
    CommunityLevelDamageAssessmentForm,
    DamageAssessmentFormCommunityV2,
    DisplacementProfilePhoneSurvey,
    DisplacementTrackingMatrixForm,
    DurableSolutionRelocationSurvey,
    RapidAssessmentFormAreaCouncil,
    ServiceMonitoringTool2026,
)
from .serializers import (
    CommunityLevelDamageAssessmentFormSerializer,
    DamageAssessmentFormCommunityV2Serializer,
    DisplacementProfilePhoneSurveySerializer,
    DisplacementTrackingMatrixFormSerializer,
    DurableSolutionRelocationSurveySerializer,
    RapidAssessmentFormAreaCouncilSerializer,
    ServiceMonitoringTool2026Serializer,
)

# -----------------------------------------------------------------------------
# Durable Solution & Relocation Survey
# -----------------------------------------------------------------------------


class DurableSolutionRelocationSurveyListCreateView(ListCreateAPIView):
    queryset = DurableSolutionRelocationSurvey.objects.all()
    serializer_class = DurableSolutionRelocationSurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DurableSolutionRelocationSurveyFilter
    ordering_fields = ["created_at", "updated_at"]


class DurableSolutionRelocationSurveyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DurableSolutionRelocationSurvey.objects.all()
    serializer_class = DurableSolutionRelocationSurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Service Monitoring Tool 2026
# -----------------------------------------------------------------------------


class ServiceMonitoringTool2026ListCreateView(ListCreateAPIView):
    queryset = ServiceMonitoringTool2026.objects.all()
    serializer_class = ServiceMonitoringTool2026Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ServiceMonitoringTool2026Filter
    ordering_fields = ["created_at", "updated_at"]


class ServiceMonitoringTool2026DetailView(RetrieveUpdateDestroyAPIView):
    queryset = ServiceMonitoringTool2026.objects.all()
    serializer_class = ServiceMonitoringTool2026Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Displacement Tracking Matrix Form
# -----------------------------------------------------------------------------


class DisplacementTrackingMatrixFormListCreateView(ListCreateAPIView):
    queryset = DisplacementTrackingMatrixForm.objects.all()
    serializer_class = DisplacementTrackingMatrixFormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DisplacementTrackingMatrixFormFilter
    ordering_fields = ["created_at", "updated_at"]


class DisplacementTrackingMatrixFormDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DisplacementTrackingMatrixForm.objects.all()
    serializer_class = DisplacementTrackingMatrixFormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Rapid Assessment Form (Area Council)
# -----------------------------------------------------------------------------


class RapidAssessmentFormAreaCouncilListCreateView(ListCreateAPIView):
    queryset = RapidAssessmentFormAreaCouncil.objects.all()
    serializer_class = RapidAssessmentFormAreaCouncilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RapidAssessmentFormAreaCouncilFilter
    ordering_fields = ["created_at", "updated_at"]


class RapidAssessmentFormAreaCouncilDetailView(RetrieveUpdateDestroyAPIView):
    queryset = RapidAssessmentFormAreaCouncil.objects.all()
    serializer_class = RapidAssessmentFormAreaCouncilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Community Level Damage Assessment Form
# -----------------------------------------------------------------------------


class CommunityLevelDamageAssessmentFormListCreateView(ListCreateAPIView):
    queryset = CommunityLevelDamageAssessmentForm.objects.all()
    serializer_class = CommunityLevelDamageAssessmentFormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CommunityLevelDamageAssessmentFormFilter
    ordering_fields = ["created_at", "updated_at"]


class CommunityLevelDamageAssessmentFormDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CommunityLevelDamageAssessmentForm.objects.all()
    serializer_class = CommunityLevelDamageAssessmentFormSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Displacement Profile - Phone Survey
# -----------------------------------------------------------------------------


class DisplacementProfilePhoneSurveyListCreateView(ListCreateAPIView):
    queryset = DisplacementProfilePhoneSurvey.objects.all()
    serializer_class = DisplacementProfilePhoneSurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DisplacementProfilePhoneSurveyFilter
    ordering_fields = ["created_at", "updated_at"]


class DisplacementProfilePhoneSurveyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DisplacementProfilePhoneSurvey.objects.all()
    serializer_class = DisplacementProfilePhoneSurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------------------------------------------------------------
# Damage Assessment Form (Community V2)
# -----------------------------------------------------------------------------


class DamageAssessmentFormCommunityV2ListCreateView(ListCreateAPIView):
    queryset = DamageAssessmentFormCommunityV2.objects.all()
    serializer_class = DamageAssessmentFormCommunityV2Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DamageAssessmentFormCommunityV2Filter
    ordering_fields = ["created_at", "updated_at"]


class DamageAssessmentFormCommunityV2DetailView(RetrieveUpdateDestroyAPIView):
    queryset = DamageAssessmentFormCommunityV2.objects.all()
    serializer_class = DamageAssessmentFormCommunityV2Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
