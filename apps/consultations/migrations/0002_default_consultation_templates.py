from dataclasses import dataclass
from decimal import Decimal

from django.db import migrations, models


@dataclass
class ConsultationTemplateData:
    """Represent consultation template data."""

    duration: int
    cost: Decimal
    fee: Decimal


DEFAULT_CONSULTATION_TEMPLATES = [
    ConsultationTemplateData(duration=20, cost=30, fee=5),
    ConsultationTemplateData(duration=40, cost=60, fee=5),
    ConsultationTemplateData(duration=60, cost=90, fee=5),
]


def create_default_consultation_templates(apps, schema_editor) -> None:
    """Create default consultation templates."""
    ConsultationTemplate = apps.get_model("consultations", "ConsultationTemplate")
    ConsultationTemplate.objects.bulk_create(
        [
            ConsultationTemplate(
                duration=template.duration,
                cost=template.cost,
                fee=template.fee,
            )
            for template in DEFAULT_CONSULTATION_TEMPLATES
        ],
    )


def delete_default_consultation_templates(apps, schema_editor) -> None:
    """Delete default consultation templates."""
    ConsultationTemplate = apps.get_model("consultations", "ConsultationTemplate")
    ConsultationTemplate.objects.filter(
        duration__in=[template.duration for template in DEFAULT_CONSULTATION_TEMPLATES],
        cost__in=[template.cost for template in DEFAULT_CONSULTATION_TEMPLATES],
        fee__in=[template.fee for template in DEFAULT_CONSULTATION_TEMPLATES],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_default_consultation_templates,
            reverse_code=delete_default_consultation_templates,
        ),
    ]
