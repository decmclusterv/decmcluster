from rest_framework import serializers

from .models import (
    CommunityLevelDamageAssessmentForm,
    DamageAssessmentFormCommunityV2,
    DisplacementProfilePhoneSurvey,
    DisplacementTrackingMatrixForm,
    DurableSolutionRelocationSurvey,
    RapidAssessmentFormAreaCouncil,
    ServiceMonitoringTool2026,
)


class DurableSolutionRelocationSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = DurableSolutionRelocationSurvey
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ServiceMonitoringTool2026Serializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMonitoringTool2026
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DisplacementTrackingMatrixFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplacementTrackingMatrixForm
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class RapidAssessmentFormAreaCouncilSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapidAssessmentFormAreaCouncil
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CommunityLevelDamageAssessmentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityLevelDamageAssessmentForm
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DisplacementProfilePhoneSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplacementProfilePhoneSurvey
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DamageAssessmentFormCommunityV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = DamageAssessmentFormCommunityV2
        fields = ["id", "field", "data", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
