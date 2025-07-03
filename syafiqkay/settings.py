# Custom 403 handler for admin and all views
from django.conf import settings
from django.conf.urls import handler403

def custom_permission_denied_view(request, exception=None):
    from django.shortcuts import render
    return render(request, "403.html", status=403)

handler403 = "syafiqkay.settings.custom_permission_denied_view"
# Load environment variables from .env before anything else
from dotenv import load_dotenv # type: ignore
load_dotenv()

# Path settings
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
import os
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")  # Secret key for cryptographic signing (safe fallback for local dev)

"""
Set DEBUG based on environment variable DJANGO_DEBUG.
If not set, default to False for safety.
Set DJANGO_DEBUG=True in your .env for local development.
"""
DEBUG = False

ALLOWED_HOSTS = [
    'syafiqkay.com',
    'www.syafiqkay.com',
    'localhost',
    '127.0.0.1',
    'syafiq-kay.onrender.com',  # Render.com deployment (old)
    'syafiq-kay.onrender.com:10000',  # Render.com deployment with port (old)
    'syafiq-kay-1.onrender.com',  # Render.com deployment (new)
    'sk-dxgmhag5dtcsamfh.uksouth-01.azurewebsites.net',  # Azure App Service deployment
]

# CSRF trusted origins for production and staging
CSRF_TRUSTED_ORIGINS = [
    "https://syafiqkay.com",
    "https://www.syafiqkay.com",
    "https://syafiq-kay-1.onrender.com",
    "https://sk-dxgmhag5dtcsamfh.uksouth-01.azurewebsites.net",
    "https://syafiq-kay.onrender.com",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',         # Admin site
    'django.contrib.auth',          # Authentication framework
    'django.contrib.contenttypes',  # Content type system (permissions, generic relations)
    'django.contrib.sessions',      # Session framework
    'django.contrib.messages',      # Messaging framework (flash messages)
    'django.contrib.staticfiles',   # Static file management
    # Project apps
    'syafiqkay.apps.SyafiqkayConfig',  # Main project app with admin customizations
    'homepage',                     # Custom app: homepage
    'journals',                     # Custom app: journals
    'noto_garden',                   # Custom app: noto_garden
<<<<<<< HEAD
    'reference',
    'experiments',                    # Custom app: reference
=======
>>>>>>> 1b750c1 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
    'storages',                   # Django-storages for cloud storage backends
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Security enhancements (e.g., HTTPS, HSTS)
    'django.contrib.sessions.middleware.SessionMiddleware',   # Session management
    'django.middleware.common.CommonMiddleware',              # Common HTTP features (e.g., URL normalization)
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Associates users with requests using sessions
    'django.contrib.messages.middleware.MessageMiddleware',   # Temporary messages for users
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Prevent clickjacking
]

# URL configuration
ROOT_URLCONF = 'syafiqkay.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'syafiqkay.wsgi.application'

<<<<<<< HEAD
# --- Azure SQL Database Configuration ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
=======
# --- For production (SQL Server) ---
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',  # Use 'mssql' for mssql-django backend
#         'NAME': os.environ.get('AZURE_SQL_DB_NAME'),
#         'USER': os.environ.get('AZURE_SQL_DB_USER'),
#         'PASSWORD': os.environ.get('AZURE_SQL_DB_PASSWORD'),
#         'HOST': os.environ.get('AZURE_SQL_DB_HOST'),
#         'PORT': os.environ.get('AZURE_SQL_DB_PORT', '1433'),
#         'OPTIONS': {
#             'driver': 'ODBC Driver 18 for SQL Server',
#             'authentication': 'ActiveDirectoryPassword',
#             'extra_params': 'Encrypt=yes;TrustServerCertificate=yes;MARS_Connection=yes;trusted_connection=no;',
#         },
#     }
# }

# --- PostgreSQL Database Configuration on Render ---
import dj_database_url
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=600)
    }
elif all(var in os.environ for var in [
    'RENDER_POSTGRES_DB_NAME', 'RENDER_POSTGRES_USER', 'RENDER_POSTGRES_PASSWORD', 'RENDER_POSTGRES_HOST'
]):
    DB_ENGINE = os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.postgresql')
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.environ.get('RENDER_POSTGRES_DB_NAME', 'default_db_name'),
            'USER': os.environ.get('RENDER_POSTGRES_USER', 'default_user'),
            'PASSWORD': os.environ.get('RENDER_POSTGRES_PASSWORD', 'default_password'),
            'HOST': os.environ.get('RENDER_POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('RENDER_POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
>>>>>>> 1b750c1 (Refactor notoGarden app: rename to noto_garden, remove unused files, and update settings)
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- static files configuration for Azure Blob Storage ---
AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER", "static")

STATIC_LOCATION = AZURE_CONTAINER
STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
AZURE_SSL = True
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin site customization
ADMIN_SITE_HEADER = "Syafiq Kay Admin"
ADMIN_SITE_TITLE = "Syafiq Kay Admin Portal"
ADMIN_INDEX_TITLE = "Welcome to Syafiq Kay Admin Portal"

# Admin CSS
ADMIN_CSS = {
    'all': ['css/admin-extra.css']
}
