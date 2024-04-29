from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission

from apps.consultations.constants import ConsultationStatus
from apps.consultations.models import Consultation


class IsReceivedConsultation(BasePermission):
    """Check if request user receives the consultation."""

    def has_object_permission(self, request, view, obj: Consultation) -> bool:
        """Allow request only when requested user receives consultation."""
        if obj.to_user != request.user:
            return False
        return super().has_object_permission(request, view, obj)


class CanAcceptConsultation(BasePermission):
    """Check if request user can accept consultation."""

    message = _("You can't accept this consultation")

    def has_object_permission(self, request, view, obj: Consultation) -> bool:
        """Allow request only when requested user receives consultation."""
        updated_status = request.data.get("status")
        if (
            updated_status == ConsultationStatus.ACCEPTED
            and obj.to_user != request.user
        ):
            return False
        return super().has_object_permission(request, view, obj)


class CanDeclineConsultation(BasePermission):
    """Check if request user can decline consultation."""

    message = _("You can't decline this consultation")

    def has_object_permission(self, request, view, obj: Consultation) -> bool:
        """Allow request only when requested user receives consultation."""
        updated_status = request.data.get("status")
        if (
            updated_status == ConsultationStatus.DECLINED
            and obj.to_user != request.user
        ):
            return False
        return super().has_object_permission(request, view, obj)


class CanCancelConsultation(BasePermission):
    """Check if request user can cancel the consultation."""

    message = _("You can't decline this consultation")

    def has_object_permission(self, request, view, obj: Consultation) -> bool:
        """Allow request only when requested user creates consultation."""
        updated_status = request.data.get("status")
        if (
            updated_status == ConsultationStatus.CANCELLED
            and obj.status == ConsultationStatus.REQUESTED
            and obj.from_user != request.user
        ):
            return False
        return super().has_object_permission(request, view, obj)
