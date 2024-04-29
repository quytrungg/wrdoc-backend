import typing

from django.core.exceptions import ValidationError

from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    """Base model for apps' models.

    This class adds to models created and modified fields

    """

    class Meta:
        abstract = True

    def clean(self):
        """Validate model data.

        First we collect all errors as dict and then if there any errors, we
        pass them ValidationError and raise it. By doing this django admin and
        drf can specify for each field an error.

        """
        super().clean()
        errors = {}
        for field in self._meta.fields:
            clean_method = f"clean_{field.name}"
            if hasattr(self, clean_method):
                try:
                    getattr(self, clean_method)()
                except ValidationError as error:
                    errors[field.name] = error
        if errors:
            raise ValidationError(errors)


BaseModelAncestor = typing.TypeVar("BaseModelAncestor", bound=BaseModel)
