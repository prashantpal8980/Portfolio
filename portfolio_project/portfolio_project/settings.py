"""
Django settings for portfolio_project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ─── BASE DIR ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (local dev only; hosting platforms
# inject them directly as env vars so .env is optional in production)
load_dotenv(BASE_DIR / '.env')

# ─── CORE SECRETS ────────────────────────────────────────────────────────────
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']   # Will raise KeyError if missing — intentional

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# Comma-separated hosts in .env, e.g.: ALLOWED_HOSTS=memorygallery.space,www.memorygallery.space
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

# ─── APPLICATION ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.portfolio',
]

INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# ─── DATABASE ─────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── PASSWORD VALIDATION ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── INTERNATIONALISATION ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── STATIC & MEDIA FILES ─────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # served by Nginx / whitenoise in prod

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── AUTH REDIRECTS ───────────────────────────────────────────────────────────
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ─── CSRF ─────────────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://prashantpal.online',
    'https://www.prashantpal.online',
    
]

# ─── PRODUCTION SECURITY SETTINGS ─────────────────────────────────────────────
# These activate automatically when DEBUG=False (i.e. in production).
# They have zero effect in local dev.

if not DEBUG:
    # Force HTTPS — redirect all HTTP requests to HTTPS
    SECURE_SSL_REDIRECT = True

    # Tell browsers to only use HTTPS for this site for 1 year (HSTS)
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Do not allow the browser to guess/sniff content types
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Protect against XSS attacks via browser heuristic
    SECURE_BROWSER_XSS_FILTER = True

    # Session cookie only sent over HTTPS
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF cookie only sent over HTTPS
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    # Prevent the site from being embedded in iframes on other domains
    X_FRAME_OPTIONS = 'DENY'

    # Referrer header policy
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ─── UPLOAD LIMITS ────────────────────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024   # 20 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024   # 20 MB

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
