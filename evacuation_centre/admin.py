from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import EvacuationCentre, EvacuationCentreImport


@admin.register(EvacuationCentre)
class EvacuationCentreAdmin(ModelAdmin):
    list_display = (
        "compound_name",
        "organization",
        "agency",
        "province",
        "area_council",
        "latitude",
        "longitude",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "province",
        "organization",
        "is_ec_owner_approved",
        "is_ec_govt_approved",
    )
    search_fields = (
        "compound_name",
        "organization",
        "agency",
        "province",
        "area_council",
        "island",
        "village",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(EvacuationCentreImport)
class EvacuationCentreImportAdmin(ModelAdmin):
    list_display = (
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
        "file",
        "uploaded_by__email",
        "uploaded_by__first_name",
        "uploaded_by__last_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
