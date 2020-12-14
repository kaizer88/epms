# settings/local.py

from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails/app-messages'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'epms',
<<<<<<< HEAD
        # 'USER': 'epmuser',
        'USER': 'postgres',
        'PASSWORD': 'Lihle@2016',
        # 'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 'udms_path': settings.LOCAL_UDMS_WEB_DIR+"/"+ibookref+"/"
#
# {% if message.type == "PHONELOG" %}
#                         <td>{{ message.folder }}</td>
#                     {% elif message.type == "CONFIRMATION" %}
#                         <td><a href="{{ udms_path}}{{ message.folder }}"->{{ message.folder }}</a></td>
#                     {% else %}
#                         <td><a href="{% url 'system_reservations_emails_main:emails_display' booking_ref=message.booking_folder message_no=message.order%}">{{ message.folder }}</a></td>
#                     {% endif %}
=======
        'USER': 'epmuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
>>>>>>> master
