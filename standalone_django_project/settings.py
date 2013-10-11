import os

ACTIONKIT_EVENT_UPLOADER_PROCESSING_METHOD = "sync"

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ROOT_URLCONF = 'standalone_django_project.urls'
WSGI_APPLICATION = 'standalone_django_project.wsgi.application'
SITE_ID = 1

SITE_NAME = os.environ.get("SITE_NAME")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "http://localhost:8080")
import urlparse
ALLOWED_HOSTS = [urlparse.urlparse(SITE_DOMAIN).hostname]

if os.environ.get('DJANGO_DEBUG'):
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ["DJANGO_SECRET"]

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),
    }

plugins = []
import pkg_resources
for app in pkg_resources.iter_entry_points("django.plugins"):
    app = app.load()
    plugins.append(app)

for p in plugins:
    dbs = getattr(p, 'DATABASES', {})
    for key, value in dbs.items():
        DATABASES[key] = value

TEMPLATE_LOADERS = (
    'dbtemplates.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',

    'south',

    'django.contrib.flatpages',

    'djangohelpers', 
    'dbtemplates',

    'standalone_django_project',  # For the template finder

    'apihangar',
    'actionkit',
]

for p in plugins:
    apps = getattr(p, 'INSTALLED_APPS', None)
    if apps:
        INSTALLED_APPS.extend(apps)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "standalone_django_project.context_processors.globals",
)

for p in plugins:
    ctx = getattr(p, 'CONTEXT_PROCESSORS', None)
    if ctx:
        CONTEXT_PROCESSORS.extend(ctx)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

for p in plugins:
    auths = getattr(p, 'AUTHENTICATION_BACKENDS', None)
    if auths:
        AUTHENTICATION_BACKENDS.extend(auths)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',

    "djangohelpers.middleware.AuthRequirementMiddleware",
    "djangohelpers.middleware.PermissionsMiddleware",
)

for p in plugins:
    apps = getattr(p, 'MIDDLEWARE_CLASSES', None)
    if apps:
        MIDDLEWARE_CLASSES.extend(apps)

ANONYMOUS_PATHS = [
    "/static/",
    "/admin/",
    "/accounts/",
    ]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

if os.environ.get('DJANGO_DEBUG_TOOLBAR'):
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        )
    INSTALLED_APPS += (
        'debug_toolbar',
        )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        }
    INTERNAL_IPS = os.environ.get("INTERNAL_IPS")
    if INTERNAL_IPS is None:
        INTERNAL_IPS = ['127.0.0.1']
    elif INTERNAL_IPS.strip() in ("*", "0.0.0.0"):
        class AllIPS(list):
            def __contains__(self, item):
                return True
        INTERNAL_IPS = AllIPS()
    else:
        INTERNAL_IPS = [i.strip() for i in INTERNAL_IPS.split()]

STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')

APIHANGAR_DATABASES = os.environ.get("APIHANGAR_DATABASES") or ""
APIHANGAR_DATABASES = [d.strip() for d in APIHANGAR_DATABASES.split()
                       if d.strip() in DATABASES]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

PLUGIN_URLCONFS = []
for p in plugins:
    apps = getattr(p, 'URLCONFS', None)
    if apps:
        PLUGIN_URLCONFS.extend(apps)

for p in plugins:
    settings = getattr(p, 'SETTINGS', None)
    if settings:
        for setting in settings:
            locals()[setting] = settings[setting]
del plugins
