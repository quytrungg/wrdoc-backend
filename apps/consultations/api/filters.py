from django_filters import rest_framework as filters

from apps.consultations.constants import ConsultationStatus
from apps.consultations.models import Consultation


# pylint: disable=unused-argument
class ConsultationFilter(filters.FilterSet):
    """Represent filters in Consultation CRUD."""

    status = filters.ChoiceFilter(choices=ConsultationStatus.choices)
    requested_from = filters.BooleanFilter(method="filter_by_request_from")
    requested_to = filters.BooleanFilter(method="filter_by_request_to")

    def filter_by_request_from(self, queryset, name, value):
        """Filter consultations that are requested from the user."""
        if value is True:
            return queryset.filter(from_user=self.request.user)
        return queryset

    def filter_by_request_to(self, queryset, name, value):
        """Filter consultations that are requested to the user."""
        if value is True:
            return queryset.filter(to_user=self.request.user)
        return queryset

    class Meta:
        model = Consultation
        fields = (
            "status",
        )
