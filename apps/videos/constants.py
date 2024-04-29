from django.db.models import TextChoices

VIDEO_EXP_TIME_EPOCH = 60 * 60 * 24  # 24 hours


class VideoRole(TextChoices):
    """Represent video roles."""

    HOST = "1", "Host/Co-host"
    PARTICIPANT = "0", "Participant"
