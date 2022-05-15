import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Class for custom Django management command which be registered in the manage.py
       This command will attempt to make connections to the db until successful."""

    def handle(self, *args, **options):
        conn = None
        while conn is None:
            try:
                conn = connections['default'] # attempt connecting to default db
            except OperationalError:
                self.stdout.write('Could not connect to database, retrying in 1s...')
                time.sleep(1)

        self.stdout.write('Connected to database successfully')