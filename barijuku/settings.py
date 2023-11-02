from pathlib import Path
from dotenv import load_dotenv
import os

# import environ

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(dotenv_path)


# env = environ.Env()
# env.read_env(os.path.join(BASE_DIR,'.env'))
# env.read_env('.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7t)yfk3_1cse=udmkr4ha$3f6!qv6v$c0vej@d@0u6f4nede$h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', '.barijuku.com', 'localhost']
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app.apps.AppConfig",
    "student.apps.StudentConfig",
    "trainer.apps.TrainerConfig",
    # 'accounts.apps.AccountsConfig',
    "user.apps.UserConfig",
    "widget_tweaks",
    "calendar",
    "shop.apps.ShopConfig",
    # 'accounts',
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount'
    # 'material',
    # 'material.admin',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "barijuku.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {"calendar": "templatetags.calendar"},
        },
    },
]

WSGI_APPLICATION = "barijuku.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "barijuku_db",
        "USER": "barijuku",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "3306",
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Add this line


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
# DISABLE_USERNAME = False
# if DISABLE_USERNAME:
#     SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

# LOGIN_VIA_EMAIL = False
# USE_REMEMBER_ME = True
LOGIN_REDIRECT_URL = "/user/login/"
# LOGIN_URL = 'accounts:log_in'
LOGOUT_REDIRECT_URL = "user:login"


DAILY_SCHEDULE = [
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
    "22:00",
    "22:30",
    "23:00",
]

# STRIPE_CLIENT_ID = env('STRIPE_CLIENT_ID')
# STRIPE_CLIENT_SECRET = env('STRIPE_CLIENT_SECRET')

# ENDPOINT_SECRET = env('ENDPOINT_SECRET')

# OPENAI_API_KEY = env('OPENAI_API_KEY')
STRIPE_CLIENT_ID = os.environ["STRIPE_CLIENT_ID"]
STRIPE_CLIENT_SECRET = os.environ["STRIPE_CLIENT_SECRET"]
ENDPOINT_SECRET = os.environ["ENDPOINT_SECRET"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DEEPL_API_KEY = os.environ["DEEPL_API_KEY"]


AUTH_USER_MODEL = "user.CustomUser"
