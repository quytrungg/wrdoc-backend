from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

PHONE_NUMBER_LENGTH = 10


class UserRole(TextChoices):
    """Represent available roles for User."""

    CLINICIAN = "clinician", _("Clinician")
    STUDENT = "student", _("Student")


class ClinicianType(TextChoices):
    """Represent available clinician types."""

    CRNA = "crna", _("Certified Registered Nurse Anesthetist (CRNA)")
    NP = "np", _("Nurse Practitioner (NP)")
    PA = "pa", _("Physician Assistant (PA)")
    PA_AA = "pa_aa", _("Physician Assistant - Anesthesia Assistant (PA-AA)")
    DO = "do", _("Physician: Doctor of Osteopathy (DO)")
    MD = "md", _("Physician: Medical Doctor (MD)")
    STU = "stu", _("Student/In-Training")


class PrivacyOptions(TextChoices):
    """Represent available privacy options."""

    PUBLIC = "public", _("Public")
    CONTACTS = "contacts", _("My Contacts")
    ONLY_ME = "only_me", _("Only Me")
    CUSTOM = "custom", _("Custom group")
    CUSTOM_INV = "custom_inv", _("Custom group Inverse")


class PrivacyFields(TextChoices):
    """Fields for privacy restriction."""

    ABOUT_ME = "about_me", _("About me")
    SPECIALITY = "speciality", _("Specialty")
    PRACTICE_AREA = "practice_area", _("Current area of Practice/Speciality")


SPECIALTY_TYPES = (
    ("anesthesia", _("Anesthesia")),
    ("dermatology", _("Dermatology")),
    ("ent", _("Ear, Nose and Throat")),
    ("emergency_medicine", _("Emergency Medicine")),
    ("family_medicine", _("Family Medicine")),
    ("hospitalist", _("Hospitalist")),
    ("internal_medicine", _("Internal Medicine")),
    ("neurology", _("Neurology")),
    ("nuclear_medicine", _("Nuclear Medicine")),
    ("obstetrics_gynecology", _("Obstetrics and Gynecology")),
    ("ophthalmology", _("Ophthalmology")),
    ("otolaryngology", _("Otolaryngology (Head and Neck Surgery)")),
    ("pathology", _("Pathology")),
    ("pediatrics", _("Pediatrics")),
    ("physical_medicine", _("Physical Medicine and Rehabilitation")),
    ("psychiatry", _("Psychiatry")),
    ("radiology", _("Radiology")),
    ("surgical_assistant", _("Surgical (first) Assistant")),
    ("surgery_cardiothoracic", _("Surgery, Cardiothoracic")),
    ("surgery_general", _("Surgery, General and Trauma")),
    ("surgery_body", _("Surgery, Interventional/Endovascular - Body")),
    ("surgery_neuro", _("Surgery, Interventional/Endovascular - Neuro")),
    ("sugery_orthopaedic", _("Surgery, Orthopaedic")),
    ("sugery_neurological", _("Surgery, Neurological")),
    ("surgery_plastic", _("Surgery, Plastic")),
    ("sugery_vascular", _("Surgery, Vascular")),
    ("urgent_care", _("Urgent Care")),
    ("urology", _("Urology")),
    ("other", _("Other (please enter)")),
)
