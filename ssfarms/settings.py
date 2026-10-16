import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# -----------------------------------------------------------------------------
# CORE APPLICATION SETTINGS
# -----------------------------------------------------------------------------

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()

if not DEBUG:
    if not SECRET_KEY:
        raise ValueError(
            "CRITICAL SECURITY CONFIGURATION ERROR: "
            "The SECRET_KEY environment variable is missing in production!"
        )
    if SECRET_KEY.startswith("django-insecure-"):
        raise ValueError(
            "CRITICAL SECURITY CONFIGURATION ERROR: "
            "A development 'django-insecure-' key cannot be used when DEBUG=False!"
        )
else:
    if not SECRET_KEY:
        SECRET_KEY = "django-insecure-dev-fallback-key-do-not-use-in-production-environments"

# Parse comma-separated ALLOWED_HOSTS with safe defaults for local development
allowed_hosts_env = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,.onrender.com"
)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(",") if host.strip()]

# Parse comma-separated CSRF_TRUSTED_ORIGINS
csrf_trusted_env = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.onrender.com,http://127.0.0.1,http://localhost"
)
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in csrf_trusted_env.split(",") if origin.strip()
]

# -----------------------------------------------------------------------------
# APPLICATION DEFINITION
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Cloudinary is used for media storage only; must follow staticfiles so WhiteNoise manages static assets
    "cloudinary_storage",
    "cloudinary",
    "django.contrib.sitemaps",

    # Local farm applications
    "core",
    "products",
    "orders",
    "contact",
    "inquiry",
    "gallery",
    "testimonials",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ssfarms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "inquiry.context_processors.cart_count",
                "products.context_processors.categories_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "ssfarms.wsgi.application"

# -----------------------------------------------------------------------------
# DATABASE
# -----------------------------------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DEBUG and not DATABASE_URL:
    raise ValueError(
        "CRITICAL DATABASE CONFIGURATION ERROR: "
        "The DATABASE_URL environment variable is required when DEBUG=False! "
        "Silent fallback to SQLite in production on Render is prohibited."
    )

is_postgres = bool(DATABASE_URL and ("postgres" in DATABASE_URL or "psql" in DATABASE_URL))
ssl_required = is_postgres and os.environ.get("DB_SSL_REQUIRE", "True").lower() in ("true", "1", "t")

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=ssl_required,
    )
}

# -----------------------------------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# STATIC & MEDIA FILES
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
    "MAGIC_FILE_PATH": "magic",
}

# Backward-compatibility for third-party packages (e.g. cloudinary-storage) inspecting STATICFILES_STORAGE
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" if not DEBUG else "django.contrib.staticfiles.storage.StaticFilesStorage"

# Production static files use WhiteNoise compressed manifest storage
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"
        if os.environ.get("CLOUDINARY_CLOUD_NAME")
        else "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": STATICFILES_STORAGE,
    },
}

# -----------------------------------------------------------------------------
# BUSINESS CONFIGURATION (WHATSAPP & CONTACT)
# -----------------------------------------------------------------------------

WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "918790733189")


# -----------------------------------------------------------------------------
# EMAIL CONFIGURATION (RESEND HTTPS API)
# -----------------------------------------------------------------------------

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "contact.resend_backend.ResendEmailBackend",
)

# Resend test sender. A verified custom domain will be needed for a
# production-branded sender address.
RESEND_FROM_EMAIL = os.environ.get(
    "RESEND_FROM_EMAIL",
    "SS Farms <onboarding@resend.dev>",
)

DEFAULT_FROM_EMAIL = RESEND_FROM_EMAIL

# Keep these settings for any other code that may still use SMTP.
EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    "ssfarmswanaparthy@gmail.com",
)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "5"))# -----------------------------------------------------------------------------
# HTTPS, COOKIE & REVERSE PROXY SECURITY
# -----------------------------------------------------------------------------

# Render terminates SSL at reverse proxy and forwards X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "t")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    X_FRAME_OPTIONS = "SAMEORIGIN"

# -----------------------------------------------------------------------------
# PRODUCTION LOGGING CONFIGURATION
# -----------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module}:{lineno} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "contact": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "orders": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "inquiry": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}