# Generated by Django 4.2.10 on 2024-04-10 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_consultationrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Completed At'),
        ),
    ]
