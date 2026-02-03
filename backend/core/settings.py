"""
Django settings for core project.
Updated for PostgreSQL + Vue.js Frontend (CORS) + Django REST Framework.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(tedrm+8-a+pd=8zau4n(+dg2sqq204$vf8gcl%p$*&960r1&5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de Terceros
    'rest_framework',      # Para crear la API
    'corsheaders',         # Para permitir peticiones desde Vue
    
    # Tus Apps Locales
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DEBE IR ARRIBA DE TODO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', # Importante para CORS
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database - Configurada para PostgreSQL
# Recuerda: pip install psycopg2-binary
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mdgen_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}

# Configuración de CORS para Vue.js
# Permite que el servidor de desarrollo de Vite (normalmente puerto 5173) acceda a la API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-es' # Cambiado a español
TIME_ZONE = 'Europe/Madrid' # Ajustado a tu zona horaria
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'