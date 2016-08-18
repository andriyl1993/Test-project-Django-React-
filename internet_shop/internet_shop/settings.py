import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
PROJECT_NAME = os.path.basename(BASE_DIR)


# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l+9w34s%@qwi6st!qu8v=5-)s-(9$kp@@e7l5u888)_*p0nopl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# NOSE_PLUGINS = ['internet_shop.test_runner.TestDiscoveryPlugin']
# Application definition

INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'django_nose',
	###  my apps
	'main',
]

MIDDLEWARE_CLASSES = [
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'internet_shop.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, PROJECT_NAME, 'templates'),
		],
		'APP_DIRS': False,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'internet_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, PROJECT_NAME, 'media')
MEDIA_URL = '/media/'

def get_static_dir():
	l = []

	if os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'bower_components')):
		l.append(os.path.join(os.path.dirname(__file__), '..', 'bower_components'))

	if os.path.isdir(os.path.join(BASE_DIR, PROJECT_NAME, 'static')):
	        l.append(os.path.join(BASE_DIR, PROJECT_NAME, 'static'))
	l.append(os.path.join(BASE_DIR, 'assets'))

	return tuple(l)

STATICFILES_DIRS = get_static_dir()

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'

NOSE_ARGS = ['--nocapture',
             '--nologcapture',]