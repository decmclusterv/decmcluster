from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Newsletter


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ["email", "is_subscribed", "created_at"]
    search_fields = ["email"]
    list_filter = ["is_subscribed", "created_at"]
