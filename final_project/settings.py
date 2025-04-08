from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables from .env file (if it exists)
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Falls back to a default if not set in environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# Set environment (used for switching DB or config)
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to True for local development

# Hosts allowed to access the server
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Django REST Framework and JWT settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT token settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_BLACKLIST_ENABLED': True,
    # Use 'user_id' as primary key field if using a custom User model
    'USER_ID_FIELD': 'user_id'
}

# Applications installed in this Django project
INSTALLED_APPS = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your main app
    "group7_app.apps.Group7AppConfig",

    # Third-party packages
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",

    # Custom Django apps
    "users.apps.UsersConfig",
    "messages.apps.MessagesConfig",
    "notifications",
    "comments",
    "badges",
    "admin_tools",
    "analytics",
    "sql_app.apps.SqlAppConfig",
    "schema",
    "llm_analytics"
]

# Custom User model path
AUTH_USER_MODEL = 'users.User'

# Middleware components for request/response lifecycle
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Enables CORS
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL configuration
ROOT_URLCONF = "final_project.urls"

# Template engine configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI entry point for deployment
WSGI_APPLICATION = "final_project.wsgi.application"

# Database configuration (MySQL used here)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),  # GCP MySQL address
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
        # Reuse same DB config for test environment
        'TEST': {'MIRROR': 'default'},
    }
}

# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static file URL prefix
STATIC_URL = "static/"

# Default field type for model primary keys
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allow cross-origin requests from frontend (e.g., React at port 3000)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Allow cookies (for session-based auth if needed)
CORS_ALLOW_CREDENTIALS = True