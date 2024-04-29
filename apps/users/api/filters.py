from django.db.models import Q

from django_filters import rest_framework as filters

from apps.users.constants import ClinicianType
from apps.users.models import User


class BaseUserSearchFilter(filters.FilterSet):
    """Represent base searching filters related to User entity."""

    search = filters.CharFilter(
        method="filter_by_search",
        help_text=(
            "Search terms within these fields: username, first_name, last_name"
            ", entity, specialty, clinician_type, specialty_area"
        ),
    )

    # pylint: disable=unused-argument
    def filter_by_search(self, queryset, name, value):
        """Filter by search phrase."""
        clinician_type_filter_list = [
            code
            for code, label in ClinicianType.choices
            if value.lower() in label.lower()
        ]
        return queryset.filter(
            Q(username__icontains=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(entity__icontains=value)
            | Q(specialty__icontains=value)
            | Q(clinician_type__in=clinician_type_filter_list)
            | Q(specialty_area__icontains=value),
        )

    class Meta:
        model = User
        fields = ()


class UserFilter(BaseUserSearchFilter):
    """Represent filters in User list/retrieve API.

    It includes search by fields (icontains) and filter by fields (iexact).

    Search by fields
        - username
        - first_name
        - last_name
        - entity
        - specialty
        - clinician_type
        - specialty_area

    Filter by fields:
        - specialty
        - clinician_type

    """

    specialty_filter = filters.CharFilter(
        field_name="specialty",
        method="filter_by_specialty_exact",
        help_text="Filter with exact specialty type. E.g: 'Neurosurgery'",
    )
    clinician_type_filter = filters.ChoiceFilter(
        field_name="clinician_type",
        choices=ClinicianType.choices,
        help_text="Filter with exact clinician types",
    )

    # pylint: disable=unused-argument
    def filter_by_specialty_exact(self, queryset, name, value):
        """Filter by exact specialty."""
        return queryset.filter(specialty__contains=[value])

    class Meta:
        model = User
        fields = ()


class UserContactFilter(BaseUserSearchFilter):
    """Provide filters for User contact list API."""

    class Meta:
        model = User
        fields = ()
