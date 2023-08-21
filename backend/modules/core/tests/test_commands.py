from unittest.mock import patch
from django.test import TestCase
from django.core.management import call_command, CommandError
from django.db.utils import OperationalError


class CommandTests(TestCase):
    def test_waiting_for_db_ready(self):
        """
        test waiting for db when db is available.
        """
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)

    def test_waiting_for_db(self):
        """
        test waiting for db
        """
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 6)

    def test_waiting_for_db_timeout(self):
        """
        test waiting for db timeout
        """
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.side_effect = [OperationalError] * 100
            with self.assertRaises(CommandError) as ce:
                call_command("wait_for_db", timeout=2)
        self.assertIn(
            "Timeout: Database unavailable after 2 seconds.", str(ce.exception)
        )
