from dataclasses import dataclass

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

CONSULTATION_FEE_RATE = 0.05
TEMPLATES_COUNT = 4


class ConsultationStatus(TextChoices):
    """Represent available statuses in consultation."""

    REQUESTED = "requested", _("Requested")
    ACCEPTED = "accepted", _("Accepted")
    DECLINED = "declined", _("Declined")
    IN_PROGRESS = "in_progress", _("In Progress")
    COMPLETED = "completed", _("Completed")
    CANCELLED = "cancelled", _("Cancelled")


class SessionType(TextChoices):
    """Represent available session types in Consultation."""

    CONSULTATION = "consultation", _("Consultation")
    MENTORSHIP = "mentorship", _("Mentorship")


@dataclass
class ConsultationTemplateData:
    """Represent consultation template data."""

    session_type: str
    duration: int


DEFAULT_CONSULTATION_TEMPLATES = [
    ConsultationTemplateData(SessionType.CONSULTATION, 20),
    ConsultationTemplateData(SessionType.CONSULTATION, 40),
    ConsultationTemplateData(SessionType.MENTORSHIP, 20),
    ConsultationTemplateData(SessionType.MENTORSHIP, 40),
]


CONSULTATION_STATUS_ACTION_MAP = {
    ConsultationStatus.ACCEPTED: "accept",
    ConsultationStatus.DECLINED: "decline",
    ConsultationStatus.IN_PROGRESS: "start",
    ConsultationStatus.COMPLETED: "complete",
    ConsultationStatus.CANCELLED: "cancel",
}
