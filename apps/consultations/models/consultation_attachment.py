from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class ConsultationAttachment(BaseModel):
    """Represent images/files in a consultation request."""

    name = models.CharField(
        verbose_name=_("Image/File Name"),
        max_length=50,
        blank=True,
    )
    consultation = models.ForeignKey(
        to="consultations.Consultation",
        verbose_name=_("Consultaion ID"),
        related_name="attachments",
        on_delete=models.CASCADE,
    )
    file = models.FileField(   # noqa: DJ01
        verbose_name=_("Image/File"),
        max_length=1000,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Consultation Attachment")
        verbose_name_plural = _("Consultation Attachments")

    def __str__(self) -> str:
        return f"Attachment {self.id} for consultation {self.consultation_id}"
