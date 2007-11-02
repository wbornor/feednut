# Django settings for westom project.
import sys, os, inspect

# I added this so that we can always refer to it for the current
# document root. This will be helpful when we move to Apache
DOCUMENT_ROOT = os.getcwd()
curframe = inspect.currentframe()
try:
    DOCUMENT_ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(curframe)[0]))
finally:
    del curframe

#change this to point to where you have/want the feeds stored
FEEDS_DIR = os.path.join(DOCUMENT_ROOT, '../feeds')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

URL_HOST = 'http://localhost:8000'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'      # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
#DATABASE_NAME = ''
#DATABASE_USER = ''
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


## MAIL SETTINGS
EMAIL_HOST = ""
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = ""
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

#uncomment these on the server
#SESSION_COOKIE_DOMAIN = '.feednut.com'
#APPEND_SLASH = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '()_bph_=kn&gfbub($-wwzr=h*j1^k+0srce%x1br5z%+mk$ze'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
#    "westom.rewrite.RewiteLocalForwardedRequest",
)

ROOT_URLCONF = 'westom.urls'

TEMPLATE_DIRS = (
    os.path.join(DOCUMENT_ROOT, 'feednut/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "westom.feednut.context_processors.default",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'westom.feednut',
)


#setup the logger -- need to replace the \\ on windows
from logging.config import fileConfig
LOG_PATH = os.path.abspath(os.path.join(DOCUMENT_ROOT, '../log/feednut.log')).replace('\\', '/')
try:
    os.makedirs(os.path.dirname(LOG_PATH))
except:{}
fileConfig(os.path.join(DOCUMENT_ROOT, 'logging.config'), defaults={'log_path':LOG_PATH})