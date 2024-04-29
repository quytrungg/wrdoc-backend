from s3direct.api.fields import S3DirectUploadURLField

from apps.core.api.serializers import ModelBaseSerializer

from ...models import ConsultationAttachment


class ConsultationAttachmentSerializer(ModelBaseSerializer):
    """Represent serializer for ConsultationAttachment model."""

    file = S3DirectUploadURLField(allow_null=True)

    class Meta:
        model = ConsultationAttachment
        fields = (
            "id",
            "name",
            "file",
            "consultation_id",
        )
