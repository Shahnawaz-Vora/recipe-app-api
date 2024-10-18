"""Test django custom management commands"""
from unittest.mock import patch
from psycopg.errors import OperationalError as PsycopgOperationalError
from django.db.utils import OperationalError as DjangoOperationalError

from django.core.management import call_command
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test wait for db ready"""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting operational errors"""
        psycopg_errors = [PsycopgOperationalError("psycopg error")] * 2
        django_errors = [DjangoOperationalError("django error")] * 3
        patched_check.side_effect = psycopg_errors + django_errors + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)  # 2 + 3 + 1
        patched_check.assert_called_with(databases=['default'])
