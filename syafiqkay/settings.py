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

# Debug and allowed hosts
DEBUG = False  # Set False to test custom error pages
ALLOWED_HOSTS = [
    'syafiqkay.com',
    'www.syafiqkay.com',
    'localhost',
    '127.0.0.1',
    'syafiq-kay.onrender.com',  # Render.com deployment
    'syafiq-kay.onrender.com:10000',  # Render.com deployment with port
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
    'homepage',                     # Custom app: homepage
    'journals',                     # Custom app: journals
    'noto_garden',                   # Custom app: noto_garden
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

# --- Azure SQL Database Configuration ---
if all(var in os.environ for var in [
    'AZURE_SQL_DB_NAME', 'AZURE_SQL_DB_USER', 'AZURE_SQL_DB_PASSWORD', 'AZURE_SQL_DB_HOST'
]):
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.environ.get('AZURE_SQL_DB_NAME'),
            'USER': os.environ.get('AZURE_SQL_DB_USER'),
            'PASSWORD': os.environ.get('AZURE_SQL_DB_PASSWORD'),
            'HOST': os.environ.get('AZURE_SQL_DB_HOST'),
            'PORT': os.environ.get('AZURE_SQL_DB_PORT', '1433'),
            'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'encrypt': True,
            'trust_server_certificate': False,
            'connection_timeout': 30,
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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
