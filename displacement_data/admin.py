from django.contrib import admin

from .models import (
    CommunityLevelDamageAssessmentForm,
    DamageAssessmentFormCommunityV2,
    DisplacementProfilePhoneSurvey,
    DisplacementTrackingMatrixForm,
    DurableSolutionRelocationSurvey,
    RapidAssessmentFormAreaCouncil,
    ServiceMonitoringTool2026,
)


@admin.register(DurableSolutionRelocationSurvey)
class DurableSolutionRelocationSurveyAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(ServiceMonitoringTool2026)
class ServiceMonitoringTool2026Admin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(DisplacementTrackingMatrixForm)
class DisplacementTrackingMatrixFormAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(RapidAssessmentFormAreaCouncil)
class RapidAssessmentFormAreaCouncilAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(CommunityLevelDamageAssessmentForm)
class CommunityLevelDamageAssessmentFormAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(DisplacementProfilePhoneSurvey)
class DisplacementProfilePhoneSurveyAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(DamageAssessmentFormCommunityV2)
class DamageAssessmentFormCommunityV2Admin(admin.ModelAdmin):
    list_display = ["id", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
