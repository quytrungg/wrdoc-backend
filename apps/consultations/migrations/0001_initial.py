# Generated by Django 4.2.10 on 2024-03-13 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('duration', models.IntegerField(help_text='Duration of the session in minutes.', verbose_name='Duration')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Cost')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Fee')),
            ],
            options={
                'verbose_name': 'ConsultationTemplate',
                'verbose_name_plural': 'ConsultationTemplates',
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='requested', verbose_name='Status')),
                ('session_type', models.CharField(choices=[('consultation', 'Consultation'), ('mentorship', 'Mentorship')], verbose_name='Session Type')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Description')),
                ('note', models.TextField(blank=True, max_length=1000, verbose_name='Description')),
                ('duration', models.IntegerField(help_text='Duration of the session in minutes.', verbose_name='Duration')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Cost')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Fee')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_consultations', to=settings.AUTH_USER_MODEL, verbose_name='From User')),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='consultations.consultationtemplate', verbose_name='Template')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_consultations', to=settings.AUTH_USER_MODEL, verbose_name='To User')),
            ],
            options={
                'verbose_name': 'Consultation',
                'verbose_name_plural': 'Consultations',
            },
        ),
    ]
