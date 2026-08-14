from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import FiveWActivity, FiveWImport


@admin.register(FiveWActivity)
class FiveWActivityAdmin(ModelAdmin):
    list_display = (
        "reporting_org_name",
        "donor",
        "cluster_name",
        "state_abyei",
        "activity_status",
        "reporting_month",
        "total_beneficiaries_reached",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "activity_status",
        "reporting_month",
        "cluster_name",
        "state_abyei",
        "donor",
    )
    search_fields = (
        "reporting_org_name",
        "donor",
        "cluster_name",
        "state_abyei",
        "activity",
        "indicator",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(FiveWImport)
class FiveWImportAdmin(ModelAdmin):
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
