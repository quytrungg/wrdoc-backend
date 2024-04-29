# Generated by Django 4.2.10 on 2024-03-05 04:32

import citext.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=20, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='user',
            name='clinician_type',
            field=models.CharField(choices=[('crna', 'Certified Registered Nurse Anesthetist'), ('np', 'Nurse Practitioner'), ('pa', 'Physician Assistant'), ('pa_aa', 'Physician Assistant - Anesthesiologist Assistant'), ('do', 'Physician: Doctor of Osteopathic'), ('md', 'Physician: Medical Doctor'), ('stu', 'Student/In-Training')], default=1, max_length=50, verbose_name='Clinician Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='course_schedule',
            field=models.FileField(blank=True, max_length=1000, null=True, upload_to='', verbose_name='Course Schedule'),
        ),
        migrations.AddField(
            model_name='user',
            name='entity',
            field=models.CharField(blank=True, max_length=255, verbose_name='Entity'),
        ),
        migrations.AddField(
            model_name='user',
            name='fax_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='Fax Number'),
        ),
        migrations.AddField(
            model_name='user',
            name='graduation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Graduation Date'),
        ),
        migrations.AddField(
            model_name='user',
            name='npi_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='NPI Number'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='user',
            name='pronoun',
            field=models.CharField(blank=True, max_length=30, verbose_name='Pronoun'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('clinician', 'Clinician'), ('student', 'Student')], default=1, max_length=30, verbose_name='Role'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='secondary_email',
            field=citext.fields.CIEmailField(blank=True, max_length=254, verbose_name='Seondary Email address'),
        ),
        migrations.AddField(
            model_name='user',
            name='specialty',
            field=models.CharField(default=1, max_length=255, verbose_name='Specialty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=20, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=50, unique=True, verbose_name='Username'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Zipcode'),
        ),
    ]