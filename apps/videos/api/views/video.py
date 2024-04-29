from django.db.models import QuerySet

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...services import generate_video_jwt_signature
from .. import serializers


class VideoAuthView(GenericAPIView):
    """Viewset to provide video's auth jwt."""

    queryset = QuerySet()
    serializer_class = serializers.VideoAuthSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        """Handle post request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signature = generate_video_jwt_signature(serializer.validated_data)
        return Response(data={"signature": signature})
