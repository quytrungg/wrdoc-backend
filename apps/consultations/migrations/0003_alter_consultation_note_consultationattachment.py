# Generated by Django 4.2.10 on 2024-03-21 07:36

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_default_consultation_templates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='note',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Note'),
        ),
        migrations.CreateModel(
            name='ConsultationAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='Image/File Name')),
                ('file', models.FileField(blank=True, max_length=1000, null=True, upload_to='', verbose_name='Image/File')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='consultations.consultation', verbose_name='Consultaion ID')),
            ],
            options={
                'verbose_name': 'Consultation Attachment',
                'verbose_name_plural': 'Consultation Attachments',
            },
        ),
    ]
