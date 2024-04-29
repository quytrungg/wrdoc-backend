from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class ConsultationRate(BaseModel):
    """Represent user's rate for a consultation based on type and duration."""

    rate = models.DecimalField(
        verbose_name=_("Rate"),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    template = models.ForeignKey(
        to="consultations.ConsultationTemplate",
        verbose_name=_("Consultation Template"),
        related_name="user_rates",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User ID"),
        related_name="rates",
        on_delete=models.CASCADE,
    )
    allow_offered = models.BooleanField(
        verbose_name=_("Allow Offered"),
        default=True,
    )

    class Meta:
        verbose_name = _("Consultation Rate")
        verbose_name_plural = _("Consultation Rates")

    def __str__(self):
        return f"User {self.user_id} rate {self.rate} for {self.template_id}"

    def clean_rate(self) -> None:
        """Ensure rate must be greater than 0."""
        if isinstance(self.rate, Decimal) and self.rate <= 0:
            raise ValidationError(_("Rate must be greater than 0."))

    def clean_allow_offered(self) -> None:
        """Ensure allow_offered is True if rate is not provided."""
        if not self.rate and not self.allow_offered:
            raise ValidationError(
                _("Must allow offered if rate is not provided yet."),
            )
