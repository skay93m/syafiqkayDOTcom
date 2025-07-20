# syafiqkaydotcom/settings/test.py

from .settings import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION
import os

# Connect to local Docker PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'mydatabase'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'mysecretpassword'),
        'HOST': '127.0.0.1',  # Consistently use '127.0.0.1' for database host
        'PORT': '5432',
    }
}

# 🚫 Disable external emails during test runs
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# ⚡ Speed up password hashing for faster test execution
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# 🧪 Optional: override logging for quieter test output
LOGGING = {
    'version': 1,
    # 他のロガーによる不要な出力を防ぐため、テスト時は既存ロガーを無効化します
    'disable_existing_loggers': True,
}

# Optional but useful: stricter test isolation
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
