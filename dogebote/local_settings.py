DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '/tmp/',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

BROKER_URL = ''

WALLET_AUTH = ''
# WALLET_LOCATION = ''
WALLET_LOCATION = ''

# email for login:
SOUNDCLOUD_CLIENT_ID = ''
SOUNDCLOUD_CLIENT_SECRET = ''
SOUNDCLOUD_USERNAME = ''
SOUNDCLOUD_PASSWORD = ''
SOUNDCLOUD_USER_ID = ''
