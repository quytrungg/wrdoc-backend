from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

from ...constants import VideoRole


class VideoAuthSerializer(OpenApiSerializer):
    """Serializer for Video authentication."""

    tpc = serializers.CharField(max_length=200, help_text="Sesion name")
    role_type = serializers.ChoiceField(choices=VideoRole.choices)
    session_key = serializers.CharField(
        max_length=36,
        required=False,
        help_text="Only required for host/co-host.",
    )
    user_identity = serializers.CharField(max_length=35, required=False)

    class Meta:
        fields = (
            "tpc",
            "role_type",
            "session_key",
            "user_identity",
        )

    def validate(self, attrs):
        """Ensure session_key is provided if user is host/co-host."""
        errors = {}
        role_type = attrs["role_type"]
        session_key = attrs.get("session_key")

        if role_type == VideoRole.HOST and not session_key:
            errors["session_key"] = "Session key is required for host role."

        if errors:
            raise serializers.ValidationError(errors)
        return attrs
