# Generated by Django 5.0.4 on 2024-04-24 06:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address_zip',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Valid zip code should be XXXXX or XXXXX-XXXX', regex='^(^[0-9]{5}(?:-[0-9]{4})?$|^$)')], verbose_name='Address Zipcode'),
        ),
        migrations.AlterField(
            model_name='user',
            name='primary_region_practice_zip',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Valid zip code should be XXXXX or XXXXX-XXXX', regex='^(^[0-9]{5}(?:-[0-9]{4})?$|^$)')], verbose_name='Primary Region of Practice Zipcode'),
        ),
    ]
