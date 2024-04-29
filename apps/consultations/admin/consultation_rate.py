from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


# pylint: disable=unused-argument
@admin.register(models.ConsultationRate)
class ConsultationRateAdmin(BaseAdmin):
    """Admin UI for ConsultationRate model."""

    list_display = (
        "id",
        "template",
        "user",
        "rate",
        "allow_offered",
    )
    list_display_links = (
        "id",
    )
    readonly_fields = (
        "id",
        "template",
        "user",
    )

    def has_add_permission(self, request, *args, **kwargs):
        """Disable creation."""
        return False

    def has_delete_permission(self, request, *args, **kwargs):
        """Disable deletion."""
        return False
