from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from ..constants import CONSULTATION_FEE_RATE, SessionType


class ConsultationTemplate(BaseModel):
    """Represent a template of duration, cost and fee for consultations."""

    session_type = models.CharField(
        verbose_name=_("Session Type"),
        choices=SessionType.choices,
    )
    duration = models.IntegerField(
        verbose_name=_("Duration"),
        help_text=_("Duration of the session in minutes."),
    )
    fee = CONSULTATION_FEE_RATE

    class Meta:
        verbose_name = _("ConsultationTemplate")
        verbose_name_plural = _("ConsultationTemplates")

    def __str__(self):
        return f"{self.session_type} - {self.duration} minutes"
