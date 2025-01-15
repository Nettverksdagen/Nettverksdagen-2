EMAIL_HOST = 'postfix'

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

# Normally using port 25 is unsafe as it cannot be encrypted.
# However, all the traffic to port 25 will remain inside docker.
# After the traffic leaves docker through the mailserver, it will be on port 587.
EMAIL_PORT = '25'

EMAIL_USE_TLS = False

EMAIL_USE_SSL = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'