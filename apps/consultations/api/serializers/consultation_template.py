from apps.core.api.serializers import DecimalField, ModelBaseSerializer

from ... import models


class ConsultationTemplateSerializer(ModelBaseSerializer):
    """Represent serializer for ConsultationTemplate model."""

    fee = DecimalField()

    class Meta:
        model = models.ConsultationTemplate
        fields = (
            "id",
            "session_type",
            "duration",
            "fee",
        )
