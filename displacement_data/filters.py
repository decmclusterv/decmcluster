import django_filters

from .models import (
    CommunityLevelDamageAssessmentForm,
    DamageAssessmentFormCommunityV2,
    DisplacementProfilePhoneSurvey,
    DisplacementTrackingMatrixForm,
    DurableSolutionRelocationSurvey,
    RapidAssessmentFormAreaCouncil,
    ServiceMonitoringTool2026,
)


class BaseFormFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )


class DurableSolutionRelocationSurveyFilter(BaseFormFilter):
    class Meta:
        model = DurableSolutionRelocationSurvey
        fields = []


class ServiceMonitoringTool2026Filter(BaseFormFilter):
    class Meta:
        model = ServiceMonitoringTool2026
        fields = []


class DisplacementTrackingMatrixFormFilter(BaseFormFilter):
    class Meta:
        model = DisplacementTrackingMatrixForm
        fields = []


class RapidAssessmentFormAreaCouncilFilter(BaseFormFilter):
    class Meta:
        model = RapidAssessmentFormAreaCouncil
        fields = []


class CommunityLevelDamageAssessmentFormFilter(BaseFormFilter):
    class Meta:
        model = CommunityLevelDamageAssessmentForm
        fields = []


class DisplacementProfilePhoneSurveyFilter(BaseFormFilter):
    class Meta:
        model = DisplacementProfilePhoneSurvey
        fields = []


class DamageAssessmentFormCommunityV2Filter(BaseFormFilter):
    class Meta:
        model = DamageAssessmentFormCommunityV2
        fields = []
