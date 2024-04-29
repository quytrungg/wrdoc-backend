from django.contrib import admin

from apps.core.admin import ReadOnlyAdmin

from .. import models


@admin.register(models.ConsultationTemplate)
class ConsultationTemplateAdmin(ReadOnlyAdmin):
    """Admin UI for ConsultationTemplate model."""

    list_display = (
        "id",
        "session_type",
        "duration",
        "fee",
    )
    list_display_links = (
        "id",
    )
