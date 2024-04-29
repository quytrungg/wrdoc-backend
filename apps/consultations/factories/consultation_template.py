import factory
from factory.fuzzy import FuzzyChoice

from .. import models
from ..constants import SessionType


class ConsultationTemplateFactory(factory.django.DjangoModelFactory):
    """Factory to generate test ConsultationTemplate instance."""

    session_type = FuzzyChoice(SessionType.values)
    duration = factory.Faker("random_int", min=10, max=240)

    class Meta:
        model = models.ConsultationTemplate
