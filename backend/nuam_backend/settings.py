from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-change-me")

DJANGO_DEBUG = os.getenv("DJANGO_DEBUG", "1")
DEBUG = True if str(DJANGO_DEBUG).strip() in ("1","true","True","yes","y") else False

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "es-cl")
TIME_ZONE     = os.getenv("DJANGO_TIME_ZONE", "America/Santiago")

STATIC_URL = os.getenv("DJANGO_STATIC_URL", "/static/")
MEDIA_URL  = os.getenv("DJANGO_MEDIA_URL", "/media/")


def _first_str(x, default):
    if isinstance(x, (list, tuple)):
        x = x[0] if x else default
    return x if isinstance(x, str) else str(x)

LANGUAGE_CODE = _first_str(LANGUAGE_CODE, "es-cl")
TIME_ZONE     = _first_str(TIME_ZONE, "America/Santiago")
STATIC_URL    = _first_str(STATIC_URL, "/static/")
MEDIA_URL     = _first_str(MEDIA_URL, "/media/")
SECRET_KEY    = _first_str(SECRET_KEY, "dev-secret-change-me")


ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

ROOT_URLCONF = "nuam_backend.urls"
WSGI_APPLICATION = "nuam_backend.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATICFILES_DIRS = [ BASE_DIR / "static" ]
MEDIA_ROOT = BASE_DIR / "media"




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


     'rest_framework',
     'corsheaders',
     "django_filters",

    'taxgrades',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}


def _type(x): 
    try: return type(x).__name__
    except: return str(type(x))

print("DEBUG types =>",
      "SECRET_KEY:", _type(SECRET_KEY),
      "STATIC_URL:", _type(STATIC_URL),
      "MEDIA_URL:", _type(MEDIA_URL),
      "ROOT_URLCONF:", _type(ROOT_URLCONF),
      "WSGI_APPLICATION:", _type(WSGI_APPLICATION))
