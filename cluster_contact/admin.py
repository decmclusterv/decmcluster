from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ClusterContact


@admin.register(ClusterContact)
class ClusterContactAdmin(ModelAdmin):
    list_display = ("name", "email", "organization", "created_at")
    search_fields = ("name", "email", "organization")
    list_filter = ("created_at",)
