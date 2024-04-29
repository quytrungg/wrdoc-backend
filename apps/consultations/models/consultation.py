import typing
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import stripe.checkout

from apps.core.models import BaseModel

from ...payments.models import StripeCheckoutSession
from ...payments.services.stripe.session import create_checkout_session_payment
from ..constants import ConsultationStatus, SessionType
from ..exceptions import ConsultationActionError


# pylint: disable=duplicate-code
class Consultation(BaseModel):
    """Represent a consultation request from users to experts."""

    from_user = models.ForeignKey(
        to="users.User",
        verbose_name=_("From User"),
        related_name="created_consultations",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        to="users.User",
        verbose_name=_("To User"),
        related_name="received_consultations",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        choices=ConsultationStatus.choices,
        default=ConsultationStatus.REQUESTED,
    )
    session_type = models.CharField(
        verbose_name=_("Session Type"),
        choices=SessionType.choices,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        max_length=1000,
        blank=True,
    )
    note = models.TextField(
        verbose_name=_("Note"),
        max_length=1000,
        blank=True,
    )
    duration = models.IntegerField(
        verbose_name=_("Duration"),
        help_text=_("Duration of the session in minutes."),
    )
    cost = models.DecimalField(
        verbose_name=_("Cost"),
        max_digits=12,
        decimal_places=2,
    )
    fee = models.DecimalField(
        verbose_name=_("Fee"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Fee rate for consultation, max value is 1."),
    )
    completed_at = models.DateTimeField(
        verbose_name=_("Completed At"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")

    def __str__(self):
        return f"Consultation from {self.from_user} to {self.to_user}"

    def save(self, *args, **kwargs) -> None:
        """Set value for `completed_at` when consultation is completed."""
        if self.status == ConsultationStatus.COMPLETED:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def clean_to_user(self) -> None:
        """Ensure to_user can't be same as from_user."""
        if self.to_user == self.from_user:
            raise ValidationError(_("Can't send consultation to this user."))

    def clean_cost(self) -> None:
        """Ensure cost is greater than 0."""
        if self.cost <= 0:
            raise ValidationError(_("Cost should be greater than 0."))

    def clean_fee(self) -> None:
        """Ensure fee is less than 1."""
        if self.fee >= 1:
            raise ValidationError(_("Fee rate should be less than 1."))

    def _change_status(
        self,
        new_status: str,
        allowed_previous_statuses: typing.Iterable[str],
    ):
        """Change status of the consultation."""
        if self.status == new_status:
            raise ConsultationActionError(
                _(f"Consultation already {new_status}"),
            )
        if self.status not in allowed_previous_statuses:
            raise ConsultationActionError(
                _(f"Can't change status to {new_status} from {self.status}"),
            )
        self.status = new_status
        self.save()

    def accept(self) -> None:
        """Accept the consultation request."""
        self._change_status(
            ConsultationStatus.ACCEPTED,
            (ConsultationStatus.REQUESTED,),
        )

    def decline(self) -> None:
        """Decline the consultation request."""
        self._change_status(
            ConsultationStatus.DECLINED,
            (ConsultationStatus.REQUESTED,),
        )

    def start(self) -> None:
        """Start the consultation."""
        self._change_status(
            ConsultationStatus.IN_PROGRESS,
            (ConsultationStatus.ACCEPTED,),
        )

    def get_checkout_session(self) -> stripe.checkout.Session:
        """Return existing or new checkout session."""
        existing_session = StripeCheckoutSession.objects.filter(
            consultation=self,
            expires_at__gt=timezone.now(),
        ).last()
        if existing_session:
            return existing_session.get_stripe_data()
        session = create_checkout_session_payment(
            self.from_user.get_stripe_account().stripe_account,
            self.session_type,
            int(self.cost * 100),
            int(self.fee * self.cost * 100),
        )
        StripeCheckoutSession(
            stripe_id=session.stripe_id,
            expires_at=datetime.fromtimestamp(session.expires_at),
            consultation=self,
        ).save()
        return session

    def complete(self) -> None:
        """Complete the consultation."""
        self._change_status(
            ConsultationStatus.COMPLETED,
            (ConsultationStatus.IN_PROGRESS,),
        )

    def cancel(self) -> None:
        """Cancel the consultation."""
        self._change_status(
            ConsultationStatus.CANCELLED,
            (
                ConsultationStatus.REQUESTED,
                ConsultationStatus.ACCEPTED,
                ConsultationStatus.IN_PROGRESS,
            ),
        )
