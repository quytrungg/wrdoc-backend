import pytest

from apps.consultations.constants import ConsultationStatus
from apps.consultations.factories import (
    ConsultationFactory,
    ConsultationTemplateFactory,
)
from apps.consultations.models import Consultation, ConsultationTemplate
from apps.users.models import User


@pytest.fixture
def consultation(student_user: User, clinician_user: User) -> Consultation:
    """Generate consultation instance."""
    return ConsultationFactory(from_user=student_user, to_user=clinician_user)


@pytest.fixture
def consultations(student_user: User) -> list[Consultation]:
    """Generate list of consultations requested by student user."""
    return ConsultationFactory.create_batch(size=5, from_user=student_user)


@pytest.fixture
def template() -> ConsultationTemplate:
    """Generate consultation template instance."""
    return ConsultationTemplateFactory()


@pytest.fixture
def templates() -> list[ConsultationTemplate]:
    """Generate list of consultation templates."""
    return ConsultationTemplateFactory.create_batch(size=5)


@pytest.fixture
def accepted_consultation() -> Consultation:
    """Generate accepted consultation instance."""
    return ConsultationFactory(status=ConsultationStatus.ACCEPTED)


@pytest.fixture
def declined_consultation() -> Consultation:
    """Generate declined consultation instance."""
    return ConsultationFactory(status=ConsultationStatus.DECLINED)


@pytest.fixture
def in_progress_consultation() -> Consultation:
    """Generate in progress consultation instance."""
    return ConsultationFactory(status=ConsultationStatus.IN_PROGRESS)


@pytest.fixture
def completed_consultation() -> Consultation:
    """Generate completed consultation instance."""
    return ConsultationFactory(status=ConsultationStatus.COMPLETED)


@pytest.fixture
def cancelled_consultation() -> Consultation:
    """Generate cancelled consultation instance."""
    return ConsultationFactory(status=ConsultationStatus.CANCELLED)
