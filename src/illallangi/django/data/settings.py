import secrets
from os import environ
from pathlib import Path
from warnings import filterwarnings

import djp
from dj_database_url import config as database_config
from dotenv import load_dotenv

load_dotenv(
    override=True,
)

filterwarnings(
    action="ignore",
    message=r".*has conflict with protected namespace.*",
    category=UserWarning,
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = secrets.token_urlsafe(64)

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django_createsuperuserwithpassword",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_htmx",
    "illallangi.django.data",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "illallangi.django.data.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "illallangi.django.data.wsgi.application"

DATABASE_PATH = (
    Path(environ.get("DATA_CONFIG_DIR", BASE_DIR)) / "illallangi-django-data.db"
)

DATABASES = {
    "default": database_config(
        default=f"sqlite:///{DATABASE_PATH}",
    ),
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AIR_TRANSPORT = {}
AVIATION = {}
EDUCATION = {
    "rdf_root": environ.get("EDUCATION_RDF_ROOT", environ.get("RDF_ROOT")),
}

FITNESS = {}
MASTODON = {
    "mastodon_user": environ.get("MASTODON_USER"),
}

RESIDENTIAL = {
    "rdf_root": environ.get("RESIDENTIAL_RDF_ROOT", environ.get("RDF_ROOT")),
}

RDF = {
    "github_file_path": environ.get("RDF_GITHUB_FILE_PATH"),
    "github_repo_name": environ.get("RDF_GITHUB_REPO_NAME"),
    "github_repo_owner": environ.get("RDF_GITHUB_REPO_OWNER"),
    "github_token": environ.get("RDF_GITHUB_TOKEN"),
}

TRIPIT = {
    "tripit_access_token_secret": environ.get("TRIPIT_ACCESS_TOKEN_SECRET"),
    "tripit_access_token": environ.get("TRIPIT_ACCESS_TOKEN"),
    "tripit_client_token_secret": environ.get("TRIPIT_CLIENT_TOKEN_SECRET"),
    "tripit_client_token": environ.get("TRIPIT_CLIENT_TOKEN"),
}

djp.settings(
    globals(),
)
