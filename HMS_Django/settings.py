from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-zvv-ms(+7c)43n5tw)%_=z=49hd9_jy%u2(qimdn!4yjdo)hu@'

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'rest_framework_simplejwt.token_blacklist',

    'users',
    'customer',
    'web',
    'hospital',
    'manager',
    'doctor',
    'receptionist',
    'main',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'HMS_Django.urls'

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

WSGI_APPLICATION = 'HMS_Django.wsgi.application'




DATABASES = {
    'default': {
        "ENGINE" : "django.db.backends.postgresql_psycopg2",
        "NAME" : "hospital",
        "HOST" : "localhost",
        "USER" : "armiyah",
        "PASSWORD" : "1234",
        "PORT" : "5432"
    }
}




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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



AUTH_USER_MODEL = 'users.User'
AUTH_PROFILE_MODULE = 'users.User'



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
