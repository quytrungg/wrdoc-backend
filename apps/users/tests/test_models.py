from django.core.exceptions import ValidationError

import pytest

from .. import models


def test_unique_email_validation(user: models.User):
    """Test validation for case insensitive unique email."""
    new_user = models.User(email=user.email.upper(), password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
    assert "email" in exc.value.error_dict
