"""
Django command to wait for db up and running
"""

from typing import Any
from django.core.management.base import BaseCommand
from psycopg.errors import OperationalError as PsycopgOperationalError
from django.db.utils import OperationalError as DjangoOperationalError
import time


class Command(BaseCommand):
    """
    Django command to wait for db
    """

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Entry point for command"""
        self.stdout.write('Waiting for database... ')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOperationalError, DjangoOperationalError):
                self.stdout.write('Database unavailable, waiting 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
