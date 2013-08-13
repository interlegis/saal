DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.engine_name', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db_name',                      # Or path to database file if using sqlite3.
        'USER': 'user_name',                      # Not used with sqlite3.
        'PASSWORD': 'user_password',                  # Not used with sqlite3.
        'HOST': 'host_name',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 'port_number',                      # Set to empty string for default. Not used with sqlite3.
    }
}
