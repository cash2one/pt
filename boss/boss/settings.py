# coding: utf-8
# Django settings for boss project.

import os

DEBUG = False

TEMPLATE_DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    # ('mkh', 'mkh@putao.cn'),#一般收不到邮件，可能被屏蔽
    # ('mkh', '2455384761@qq.com'),
    ('pz', 'pz@putao.cn'),
    ('pz', 'szsxcv0514@qq.com'),
)

MANAGERS = ADMINS

# 多个数据库使用的时候要指定数据库，未指定，默认就是default
# python manage.py inspectdb --database=report > database_report
# python manage.py syncdb --database=report

if not DEBUG:
    MY_URL = 'official'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com', # ip: '112.124.195.230'
            'PORT': '',
        },
        'main': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'pt_op_total',                      # Or path to database file if using sqlite3.
            'USER': 'putao_db',                      # Not used with sqlite3.
            'PASSWORD': 'Paopao0128!',                  # Not used with sqlite3.
            'HOST': 'sp505adcda1564f.mysql.rds.aliyuncs.com',# ip: '112.124.196.153'                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        },
        'man': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_auth_admin',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com', # ip: '112.124.195.230'
            'PORT': '',
        },
        'auth_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_auth_admin',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com', # ip: '112.124.195.230'
            'PORT': '',
        },
        'report': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com', # ip: '112.124.195.230'
            'PORT': '',
        },
        'order': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_db',
            'USER': 'putao_db',
            'PASSWORD': 'Paopao0128!',
            'HOST': 'sp505adcda1564f.mysql.rds.aliyuncs.com',
            'PORT': '',
        },
        'finance': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com', # ip: '112.124.195.230'
            'PORT': '',
        },
        'cms': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_cms_db',
            'USER': 'read_op',
            'PASSWORD': 'putao2016_up',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com',
            'PORT': ''
        },
        'activity': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_activity_coupon',
            'USER': 'putao_db',
            'PASSWORD': 'Paopao0128!',
            'HOST': 'sp505adcda1564f.mysql.rds.aliyuncs.com',
            'PORT': '',
        }

    }
else:
    MY_URL = 'local'
    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.mysql',
        #     'NAME': 'pt_biz_report',
        #     'USER': 'root',
        #     'PASSWORD': '123456',
        #     'HOST': '192.168.1.247',
        #     'PORT': '',
        # },
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'root',
            'PASSWORD': 'putao1234',
            'HOST': '120.26.214.19',
            'PORT': '',
        },
        'main': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_op_total',
            'USER': 'root',
            'PASSWORD': 'qwer',
            'HOST': '192.168.1.121',
            'PORT': '',
        },
        'man': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_auth_admin',
            'USER': 'root',
            'PASSWORD': 'qwer',
            'HOST': '192.168.1.121',
            'PORT': '',
        },
        'report': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'putao_op',
            'PASSWORD': 'PuTaoApp_)9*',
            'HOST': 'rds2seb3yiymjlg8gumzv.mysql.rds.aliyuncs.com',  # ip: '112.124.195.230'
            'PORT': '',
        },
        # 'report': {
        #     'ENGINE': 'django.db.backends.mysql',
        #     'NAME': 'pt_biz_report',
        #     'USER': 'root',
        #     'PASSWORD': 'qwer',
        #     'HOST': '192.168.1.121',
        #     'PORT': '',
        # },
        'order': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_db',
            'USER': 'pt_db',
            'PASSWORD': 'pt20120128',
            'HOST': 'sp505adcda1564f.mysql.rds.aliyuncs.com',
            'PORT': '',
        },
        'finance': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_biz_report',
            'USER': 'root',
            'PASSWORD': 'qwer',
            'HOST': '192.168.1.121',
            'PORT': '',
        },
        'cms': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_cms_db',
            'USER': 'root',
            'PASSWORD': 'qwer',
            'HOST': '192.168.1.121',
            'PORT': '',
        },
        'auth_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_auth_admin',
            'USER': 'root',
            'PASSWORD': 'qwer',
            'HOST': '192.168.1.121',
            'PORT': '',
        },
        'activity': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pt_activity_coupon',
            'USER': 'root',
            'PASSWORD': 'putao1234',
            'HOST': '120.26.214.19',
            'PORT': '',
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# 只用django，DEBUG = False正式发布的版本需要增加这项
if DEBUG is False:
    # STATIC_ROOT = '/root/boss/static/'
    STATIC_ROOT = '/mnt/pt_boss/static/'
else:
    STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'), 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# SECRET_KEY = 'k58yzo99duc_&amp;_g3^)4e^1kq)(g@ri60e*vc^)yr-fp)97ih-p'
SECRET_KEY = '^&@rpuvt(sc!afs*_7k%v&-rgk8sz*2_oav+(&hl_x6189*eo%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


AUTHENTICATION_BACKENDS = (
    'common.myuserbackend.MyRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'boss.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'boss.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'main',
    'report',
    'man',
    'order',
    'finance',
    'message'
)

DATABASE_ROUTERS = ['boss.dbsettings.AppRouter']

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'pt_admin@putao.cn'
EMAIL_HOST_PASSWORD = 'putao2015'
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = False
