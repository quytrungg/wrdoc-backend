import typing

from django.db import models

if typing.TYPE_CHECKING:
    from .models import User


class UserQuerySet(models.QuerySet):
    """Provide custom queryset methods for User model."""

    def with_has_contact(self, user: "User") -> typing.Self:
        """Annotate field to indicate if user has contact with current one."""
        return self.annotate(
            has_contact=models.Exists(
                user.contacts.filter(contact=models.OuterRef("id")),
            ),
        )

    def with_total_contacts(self) -> typing.Self:
        """Annotate field to count number of contacts."""
        return self.annotate(total_contacts=models.Count("contacts"))
