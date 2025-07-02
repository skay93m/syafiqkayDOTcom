# Load environment variables from .env before anything else
from dotenv import load_dotenv
load_dotenv()

# Path settings
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Security settings
import os
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")  # Secret key for cryptographic signing (safe fallback for local dev)

# Debug and allowed hosts
DEBUG = True  # Set True for local development to see error details
ALLOWED_HOSTS = [
    'syafiqkay.com',
    'www.syafiqkay.com',
    'syafiqkay.local',
    'localhost',
    '127.0.0.1',
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
    'notoGarden',                   # Custom app: notoGarden
    'storages',
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

# --- For local development (SQLite) ---
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# --- PostgreSQL Database Configuration on Render ---
import dj_database_url
DATABASES = {
    'default': dj_database_url.config({
        default= os.environ.get('DATABASE_URL'),
        conn_max_age=600  # Connection max age in seconds
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

# Static files (CSS, JavaScript, Images) with Azure Blob Storage
# Use django-storages and Azure Blob Storage for serving static files in production
# AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')  # Azure Storage account name
# AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')    # Azure Storage account key
# AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'static')  # Azure Blob container name

# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'  # Use Azure backend for static files
# AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'  # Azure Blob domain
# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'     # Public URL for static files

# --- static files configuration ---
STATIC_URL = '/static/'  # URL to access static files
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional directories to search for
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where static files will be collected

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
