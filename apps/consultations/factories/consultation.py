import factory
from factory.fuzzy import FuzzyChoice

from .. import models
from ..constants import CONSULTATION_FEE_RATE, SessionType


class ConsultationFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Consultation instance."""

    from_user = factory.SubFactory("apps.users.factories.UserFactory")
    to_user = factory.SubFactory("apps.users.factories.UserFactory")
    session_type = FuzzyChoice(SessionType.values)
    description = factory.Faker("sentence")
    note = factory.Faker("sentence")
    duration = factory.Faker("random_int", min=10, max=240)
    cost = factory.Faker(
        "pydecimal",
        left_digits=10,
        right_digits=2,
        positive=True,
    )
    fee = CONSULTATION_FEE_RATE

    class Meta:
        model = models.Consultation
