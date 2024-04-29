import typing

from apps.consultations import models

if typing.TYPE_CHECKING:
    from apps.users.models import User


def create_default_consultation_rates(
    user: "User",
    save: bool = True,
) -> list[models.ConsultationRate]:
    """Create default consultation rates for user."""
    rates = [
        models.ConsultationRate(user_id=user.pk, template_id=template_id)
        for template_id in models.ConsultationTemplate.objects.values_list(
            "id",
            flat=True,
        )
    ]
    if save:
        models.ConsultationRate.objects.bulk_create(rates)
    return rates
