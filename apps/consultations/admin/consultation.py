from django.contrib import admin

from apps.core.admin import BaseAdmin

from .. import models
from ..constants import ConsultationStatus


# pylint: disable=unused-argument
@admin.register(models.Consultation)
class ConsultationAdmin(BaseAdmin):
    """Admin UI for Consultation model."""

    list_display = (
        "from_user",
        "to_user",
        "session_type",
        "status",
        "duration",
        "cost",
        "fee",
    )
    readonly_fields = (
        "completed_at",
    )
    list_display_links = (
        "from_user",
        "to_user",
    )
    search_fields = (
        "from_user__username",
        "to_user__username",
    )
    fieldsets = (
        (
            "Consultation Information", {
                "fields": (
                    "from_user",
                    "to_user",
                    "description",
                    "note",
                    "session_type",
                    "status",
                    "completed_at",
                ),
            },
        ),
        (
            "Consultation Details", {
                "fields": (
                    "duration",
                    "cost",
                    "fee",
                ),
            },
        ),
    )
    actions = (
        "accept_consultation",
        "decline_consultation",
        "start_consultation",
        "complete_consultation",
        "cancel_consultation",
    )

    def accept_consultation(self, request, queryset):
        """Mark selected consultations as accepted."""
        queryset = queryset.filter(status=ConsultationStatus.REQUESTED)
        queryset.update(status=ConsultationStatus.ACCEPTED)

    accept_consultation.short_description = "Accept selected consultations"

    def decline_consultation(self, request, queryset):
        """Mark selected consultations as declined."""
        queryset = queryset.filter(status=ConsultationStatus.REQUESTED)
        queryset.update(status=ConsultationStatus.DECLINED)

    decline_consultation.short_description = "Decline selected consultations"

    def start_consultation(self, request, queryset):
        """Mark selected consultations as in progress."""
        queryset = queryset.filter(status=ConsultationStatus.ACCEPTED)
        queryset.update(status=ConsultationStatus.IN_PROGRESS)

    start_consultation.short_description = "Start selected consultations"

    def complete_consultation(self, request, queryset):
        """Mark selected consultations as completed."""
        queryset = queryset.filter(status=ConsultationStatus.IN_PROGRESS)
        queryset.update(status=ConsultationStatus.COMPLETED)

    complete_consultation.short_description = "Complete selected consultations"

    def cancel_consultation(self, request, queryset):
        """Mark selected consultations as cancelled."""
        queryset = queryset.filter(
            status__in=(
                ConsultationStatus.IN_PROGRESS,
                ConsultationStatus.ACCEPTED,
            ),
        )
        queryset.update(status=ConsultationStatus.CANCELLED)

    cancel_consultation.short_description = "Cancel selected consultations"
