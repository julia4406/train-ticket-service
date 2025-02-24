"""
Django settings for train_ticket_service project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4b+b_)2xloubdm5$$gu)0$r8-+=y&m2yny91!+up#pp6" "=-u4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_filters",
    "debug_toolbar",
    "trip",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "train_ticket_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "train_ticket_service.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "user.User"

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# after dockerizing
# MEDIA_ROOT = "/vol/web/media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": None,
    "DEFAULT_PERMISSION_CLASSES": [
        "trip.permissions.IsAdminAllOrAuthenticatedReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Train Ticket Service API",
    "DESCRIPTION": "Order tickets for trips by train.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
}

# Налаштування для життєвого циклу JWT
SIMPLE_JWT = {
    # Життєвий цикл токенів:
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5000),  # час життя access-токена (
    # 10 хвилин).
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,  # видає новий refresh-токен при оновленні.
    # "BLACKLIST_AFTER_ROTATION": False,  # якщо True, старі refresh-токени додаються в чорний список.
    # "UPDATE_LAST_LOGIN": False, #  якщо True, оновлює поле last_login користувача при автентифікації.
    #
    # # Алгоритми шифрування:
    # "ALGORITHM": "HS256",   # алгоритм підпису токена (HS256)
    # "SIGNING_KEY": settings.SECRET_KEY, # ключ для підпису (settings.SECRET_KEY)
    # "VERIFYING_KEY": "",    # публічний ключ для перевірки токена (необов'язковий)
    # "AUDIENCE": None,   # аудиторія токена (None, тобто не використовується)
    # "ISSUER": None, # видавець токена (None, тобто не перевіряється)
    # "JSON_ENCODER": None,   # кастомний JSON-енкодер для токенів (None, тобто стандартний)
    # "JWK_URL": None,    # URL для отримання JSON Web Keys (JWK), якщо використовуються асиметричні ключі
    # "LEEWAY": 0,    # допустиме відхилення у часі при перевірці токена (0 секунд)
    #
    # # Автентифікація:
    # "AUTH_HEADER_TYPES": ("Bearer",),   # тип заголовка для токена (Bearer)
    # "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",   #  HTTP-заголовок для токена (HTTP_AUTHORIZATION).
    # "USER_ID_FIELD": "id",   #  поле моделі користувача для збереження ідентифікатора (id).
    # "USER_ID_CLAIM": "user_id",   # назва claim, що містить ID користувача (user_id).
    # "USER_AUTHENTICATION_RULE":
    #     "rest_framework_simplejwt.authentication.default_user_authentication_rule",   # функція для перевірки користувача при аутентифікації.
    #
    # # Типи токенів:
    # "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),   # клас токена (AccessToken).
    # "TOKEN_TYPE_CLAIM": "token_type",   # claim, що визначає тип токена (token_type).
    # "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",   # клас користувача, що використовується в токенах (TokenUser).
    #
    # # JTI (уникнення повторного використання токенів):
    # "JTI_CLAIM": "jti",   # claim, що зберігає унікальний ідентифікатор токена (jti).
    #
    # # Sliding-токени (альтернативний механізм оновлення токенів):
    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",   # claim, що зберігає час життя refresh-токена.
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),   # час життя sliding access-токена (5 хвилин).
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),   # час життя sliding refresh-токена (1 день).
    #
    # # Серіалізатори:
    # "TOKEN_OBTAIN_SERIALIZER":
    #     "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",   # серіалізатор для отримання access/refresh-токена.
    # "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",   # серіалізатор для оновлення access-токена.
    # "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",   # серіалізатор для перевірки валідності токена.
    # "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",   # серіалізатор для додавання токенів у чорний список.
    # "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",   # серіалізатор для отримання sliding-токена.
    # "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",   # серіалізатор для оновлення sliding-токена.
}
