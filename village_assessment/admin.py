from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import VillageAssessment, VillageAssessmentImport


@admin.register(VillageAssessment)
class VillageAssessmentAdmin(ModelAdmin):
    list_display = (
        "village_name",
        "province",
        "area_council",
        "assessment_date",
        "idp_present",
        "idp_individuals_total",
        "validation_status",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "province",
        "area_council",
        "idp_present",
        "validation_status",
        "assessment_date",
    )
    search_fields = (
        "village_name",
        "province",
        "area_council",
        "enumerator1_name",
        "enumerator2_name",
        "validation_status",
    )
    ordering = ("-assessment_date", "-created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(VillageAssessmentImport)
class VillageAssessmentImportAdmin(ModelAdmin):
    list_display = (
        "name",
        "file",
        "status",
        "uploaded_by",
        "verified_by",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "name",
        "file",
        "uploaded_by__email",
        "uploaded_by__first_name",
        "uploaded_by__last_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
