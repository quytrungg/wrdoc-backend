from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.ConsultationAttachment)
class ConsultationAttachmentAdmin(BaseAdmin):
    """Admin UI for ConsultationAttachment model."""

    list_display = (
        "id",
        "name",
        "consultation",
    )
    list_display_links = (
        "id",
    )
