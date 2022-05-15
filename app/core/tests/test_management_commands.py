import django.db.utils
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from unittest.mock import patch


class MgmtCommandTests(TestCase):

    # using patch to eliminate wait from sleep.time() call in wait_for_db_ready method
    @patch('time.sleep', return_value=True)
    def test_wait_for_db_ready(self, time_sleep):
        """Tests the functionality of the wait_for_db commands.
           The method should retry until the db is available

           We will mock 5 failures followed by a success to
           test the retry logic is working as expected"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.side_effect = [OperationalError] * 5 + [True]  # return 5 an operational error 5 times, then succeed
            call_command('wait_for_db_ready')
            self.assertEqual(getitem.call_count, 6)  # assert method was called 6 times
