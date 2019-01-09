import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ewx_msg_service.settings")
django.setup()

from django.contrib.auth.models import User


try:
    admin = User.objects.get(username='admin')
except:
    User.objects.create_superuser('admin', 'milker@meipian.com', '123456')
