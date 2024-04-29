import factory

from ..models import ConsultationAttachment


class ConsultationAttachmentFactory(factory.django.DjangoModelFactory):
    """Create instance of ConsultationAttachment model."""

    name = factory.Faker("word")
    file = factory.Faker("url")
    consultation = factory.SubFactory(
        "apps.consultations.factories.ConsultationFactory",
    )

    class Meta:
        model = ConsultationAttachment
