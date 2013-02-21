#-*- coding:utf8 -*-
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.  },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT':300,
    }
}

# AUTHENTICATION_PASSWORD = ''

''' UNCOMMENT FOR DEBUG TOOLBAR
INTERNAL_IPS = ('127.0.0.1',)
def update_vars(settings_vars):
    settings_vars['MIDDLEWARE_CLASSES'] = settings_vars['MIDDLEWARE_CLASSES'] + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    settings_vars['INSTALLED_APPS'] = settings_vars['INSTALLED_APPS'] + ('debug_toolbar',)
'''
