from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Displacement, DisplacementImport


@admin.register(Displacement)
class DisplacementAdmin(ModelAdmin):
    list_display = (
        "operation",
        "admin1_name",
        "admin2_name",
        "num_present_idps",
        "reporting_date",
        "displacement_reason",
        "operation_status",
        "status",
        "id"
    )
    list_filter = (
        "status",
        "operation_status",
        "admin1_name",
        "displacement_reason",
    )
    search_fields = (
        "operation",
        "admin0_name",
        "admin1_name",
        "admin2_name",
        "displacement_reason",
    )
    ordering = ("-reporting_date",)


@admin.register(DisplacementImport)
class DisplacementImportAdmin(ModelAdmin):
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
