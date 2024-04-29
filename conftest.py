"""Configuration file for pytest."""
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.module_loading import import_string

import pytest
import pytest_lazy_fixtures

from apps.users.constants import UserRole
from apps.users.factories import UserFactory
from apps.users.models import User


def pytest_configure():
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.

    """
    pytest.lazy_fixture = pytest_lazy_fixtures.lf

    settings.DEBUG = False
    settings.RESTRICT_DEBUG_ACCESS = True
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/dev/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup):
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
# pylint: disable=invalid-name
def enable_db_access_for_all_tests(django_db_setup, db):
    """Enable access to DB for all tests."""


@pytest.fixture(scope="session", autouse=True)
def temp_directory_for_media(tmp_path_factory):
    """Fixture that set temp directory for all media files.

    This fixture changes default STORAGE to filesystem and provides temp dir
    for media. PyTest cleans up this temp dir by itself after few test runs.

    """
    settings.STORAGES["default"]["BACKEND"] = (
        "django.core.files.storage.FileSystemStorage"
    )
    settings.MEDIA_ROOT = tmp_path_factory.mktemp("tmp_media")


@pytest.fixture(scope="session")
def clinician_user(django_db_blocker) -> User:
    """Create a clinician user."""
    with django_db_blocker.unblock():
        clinician = UserFactory(
            role=UserRole.CLINICIAN,
            npi_number="1234567890",
        )
        yield clinician
        clinician.delete()


@pytest.fixture(scope="session")
def student_user(django_db_blocker) -> User:
    """Create a student user."""
    with django_db_blocker.unblock():
        student = UserFactory(role=UserRole.STUDENT)
        yield student
        student.delete()


@pytest.fixture
def create_file():
    """Return a function to create uploaded file."""
    def _create_file(filename: str):
        """Return the uploaded file's url path."""
        test_file = SimpleUploadedFile(
            filename,
            b"test",
            content_type="image/png",
        )
        file_storage_cls = import_string(
            settings.STORAGES["default"]["BACKEND"],
        )
        file_storage = file_storage_cls()
        file = file_storage.save(filename, test_file)
        return file_storage.url(file)
    return _create_file
