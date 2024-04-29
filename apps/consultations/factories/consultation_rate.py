import factory

from .. import models


# pylint: disable=duplicate-code
class ConsultationRateFactory(factory.django.DjangoModelFactory):
    """Factory to generate test ConsultationRate instance."""

    rate = factory.Faker(
        "pydecimal",
        left_digits=10,
        right_digits=2,
        positive=True,
    )
    template = factory.SubFactory(
        "apps.consultations.factories.ConsultationTemplateFactory",
    )
    user = factory.SubFactory("apps.users.factories.UserFactory")

    class Meta:
        model = models.ConsultationRate
