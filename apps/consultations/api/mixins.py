from decimal import Decimal

from apps.consultations.models import Consultation


class ConsultationTotalCostMixin:
    """Mixin to calculate total cost of consultation."""

    def get_total_cost(self, consultation: Consultation) -> Decimal:
        """Calculate total cost of consultation."""
        return consultation.cost + (consultation.cost * consultation.fee)
