import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from bri.models import Username

Username.objects.create(username='admin', password='admin', role='admin')
print("Admin user created successfully!")