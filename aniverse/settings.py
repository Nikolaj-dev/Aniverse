from datetime import timedelta
from pathlib import Path
from decouple import config
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'anime_catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aniverse.urls'

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

WSGI_APPLICATION = 'aniverse.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': DB_HOST,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'PORT': DB_PORT,
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

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


STATIC_URL = config('STATIC_URL')
STATIC_ROOT = config('STATIC_ROOT')
MEDIA_URL = config('MEDIA_URL')
MEDIA_ROOT = config('MEDIA_ROOT')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": config('ACCESS_TOKEN_LIFETIME', default=31, cast=int),
    "REFRESH_TOKEN_LIFETIME": config('REFRESH_TOKEN_LIFETIME', default=31, cast=int),
    "ROTATE_REFRESH_TOKENS": config('ROTATE_REFRESH_TOKENS', default=True, cast=bool),
    "BLACKLIST_AFTER_ROTATION": config('BLACKLIST_AFTER_ROTATION', default=False, cast=bool),
    "UPDATE_LAST_LOGIN": config('UPDATE_LAST_LOGIN', default=False, cast=bool),

    "ALGORITHM": config('ALGORITHM', default="HS256"),
    "SIGNING_KEY": config('SIGNING_KEY', default=SECRET_KEY),
    "VERIFYING_KEY": config('VERIFYING_KEY', default=""),
    "AUDIENCE": config('AUDIENCE', default=None),
    "ISSUER": config('ISSUER', default=None),
    "JSON_ENCODER": config('JSON_ENCODER', default=None),
    "JWK_URL": config('JWK_URL', default=None),
    "LEEWAY": config('LEEWAY', default=0, cast=int),

    "AUTH_HEADER_TYPES": config('AUTH_HEADER_TYPES', default=("Bearer",), cast=lambda v: tuple(v.split(','))),
    "AUTH_HEADER_NAME": config('AUTH_HEADER_NAME', default="HTTP_AUTHORIZATION"),
    "USER_ID_FIELD": config('USER_ID_FIELD', default="id"),
    "USER_ID_CLAIM": config('USER_ID_CLAIM', default="user_id"),
    "USER_AUTHENTICATION_RULE": config('USER_AUTHENTICATION_RULE', default="rest_framework_simplejwt.authentication.default_user_authentication_rule"),

    "AUTH_TOKEN_CLASSES": config('AUTH_TOKEN_CLASSES', default=("rest_framework_simplejwt.tokens.AccessToken",), cast=lambda v: tuple(v.split(','))),
    "TOKEN_TYPE_CLAIM": config('TOKEN_TYPE_CLAIM', default="token_type"),
    "TOKEN_USER_CLASS": config('TOKEN_USER_CLASS', default="rest_framework_simplejwt.models.TokenUser"),

    "JTI_CLAIM": config('JTI_CLAIM', default="jti"),

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": config('SLIDING_TOKEN_REFRESH_EXP_CLAIM', default="refresh_exp"),
    "SLIDING_TOKEN_LIFETIME": config('SLIDING_TOKEN_LIFETIME', default=31, cast=int),
    "SLIDING_TOKEN_REFRESH_LIFETIME": config('SLIDING_TOKEN_REFRESH_LIFETIME', default=31, cast=int),

    "TOKEN_OBTAIN_SERIALIZER": config('TOKEN_OBTAIN_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenObtainPairSerializer"),
    "TOKEN_REFRESH_SERIALIZER": config('TOKEN_REFRESH_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenRefreshSerializer"),
    "TOKEN_VERIFY_SERIALIZER": config('TOKEN_VERIFY_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenVerifySerializer"),
    "TOKEN_BLACKLIST_SERIALIZER": config('TOKEN_BLACKLIST_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenBlacklistSerializer"),
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": config('SLIDING_TOKEN_OBTAIN_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer"),
    "SLIDING_TOKEN_REFRESH_SERIALIZER": config('SLIDING_TOKEN_REFRESH_SERIALIZER', default="rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer"),
}