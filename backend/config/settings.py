from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "corsheaders","rest_framework","rest_framework_simplejwt",
    "tenders","bids",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND":"django.template.backends.django.DjangoTemplates",
    "DIRS":[],"APP_DIRS":True,
    "OPTIONS":{"context_processors":[
        "django.template.context_processors.request","django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
if os.getenv("DATABASE_URL"):
    import urllib.parse
    u=urllib.parse.urlparse(os.getenv("DATABASE_URL"))
    DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":u.path[1:],
        "USER":u.username,"PASSWORD":u.password,"HOST":u.hostname,"PORT":u.port or 5432}}
else:
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}

AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Thimphu"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"
MEDIA_URL="/media/"; MEDIA_ROOT=BASE_DIR/"media"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
REST_FRAMEWORK={
 "DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),
 "DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticated",),
}
