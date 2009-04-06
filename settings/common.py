DEBUG = False
TEMPLATE_DEBUG = False
SEND_BROKEN_LINK_EMAILS = False
SERVER_EMAIL = "server@sociabledesign.com"
IGNORABLE_404_STARTS = ("/favicon.ico",)

# set up a shortcut for the base location of the project
import os
PROJECT_PATH = os.path.abspath(os.path.split(os.path.split(__file__)[0])[0])

ADMINS = (
    ("Dana Spiegel", "dana@sociabledesign.com"),
)

MANAGERS = ADMINS

TIME_ZONE = "US/Eastern"
LANGUAGE_CODE = "en-us"
USE_I18N = True
MEDIA_ROOT = PROJECT_PATH + "/media/"
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
#     "django.template.loaders.eggs.load_template_source",
)

TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_PATH):
    if "templates" in dirs: TEMPLATE_DIRS = TEMPLATE_DIRS + (os.path.join(root, "templates"),)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "softball.context_processors.game_record",
)

MIDDLEWARE_CLASSES = (
    # "middleware.profiler.ProfilerMiddleware",
    # "middleware.debug.DebugFooter",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.contrib.csrf.middleware.CsrfMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_pagination.middleware.PaginationMiddleware",
    # "django.middleware.gzip.GZipMiddleware",
)

ROOT_URLCONF = "urls"

SITE_ID = 1
APPEND_SLASH = True
DEFAULT_FROM_EMAIL = "no-reply@sociabledesign.com"
LOGIN_REDIRECT_URL = "/"
INTERNAL_IPS = ("127.0.0.1")

DMIGRATIONS_DIR = os.path.join(PROJECT_PATH, "migrations")

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.humanize",
    "django.contrib.redirects",
    "werkzeug",
    "dmigrations",
    "django_extensions",
    "django_mailer",
    "django_chronograph",
    "django_pagination",
    "contact_form",
    "accounts",
    "softball",
)


def break_here():
    from IPython import Shell;
    Shell.IPShellEmbed()()
