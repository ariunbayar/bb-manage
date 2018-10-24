from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not hasattr(settings, 'KAPI_LOG_MANAGER'):
            raise ImproperlyConfigured(f"Missing required environment variable 'KAPI_LOG_MANAGER'")
