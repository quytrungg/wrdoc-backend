from .paths import BASE_DIR
from libs.s3.object_key_prefix import S3UUIDPrefixKey

# Django Storages
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
S3DIRECT_URL_STRUCTURE = "https://{1}.{0}"      # {bucket}.{endpoint}
S3DIRECT_IMAGES_MIME_TYPES = (
    "image/jpeg",
    "image/png",
)
S3DIRECT_DOCUMENT_MIME_TYPES = (
    "application/pdf",
    # Doc
    "application/msword",
    # Docx
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # xlsx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # csv
    "text/csv",
    # videos
    "video/mp4",
    "video/webm",
)
S3DIRECT_DESTINATIONS = dict(
    profile_images=dict(
        key=S3UUIDPrefixKey("profile_image"),
        allowed=S3DIRECT_IMAGES_MIME_TYPES,
    ),
    course_schedules=dict(
        key=S3UUIDPrefixKey("course_schedule"),
        allowed=S3DIRECT_DOCUMENT_MIME_TYPES + S3DIRECT_IMAGES_MIME_TYPES,
    ),
    consultations=dict(
        key=S3UUIDPrefixKey("consultation"),
        allowed=S3DIRECT_DOCUMENT_MIME_TYPES + S3DIRECT_IMAGES_MIME_TYPES,
        content_length_range=(0, MAX_FILE_SIZE),
    ),
)
DEFAULT_DESTINATION = "profile_images"
