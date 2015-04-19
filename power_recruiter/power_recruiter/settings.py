"""
Django settings for power_recruiter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (BASE_DIR + '/power_recruiter/basic_site/templates/',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j#ug*57^a%d6*#ul27jsk39qd*bl8s$lo91-w9jq**&5)%r@9f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = (
    'django_jenkins',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'power_recruiter',
    'power_recruiter.basic_site',
    'power_recruiter.candidate',
    'power_recruiter.tests'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'power_recruiter.urls'

WSGI_APPLICATION = 'power_recruiter.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pr.db'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'


# Jenkins config

PROJECT_APPS = (
    'power_recruiter',
)

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pylint',
)

PYLINT_RCFILE = '.pylintrc'

MEDIA_ROOT = BASE_DIR + '/files/'
MEDIA_URL = '/files/'
if int(os.environ.get('REMOTE_DJANGO_STATIC', 0)):
    STATIC_JS_PATH = "http://127.0.0.1:8081/"
else:
    STATIC_JS_PATH = '/static/js/'