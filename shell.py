import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "louslist.settings"
django.setup()
from django.contrib.sites.models import Site
