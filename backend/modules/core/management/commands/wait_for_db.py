import time
from django.core.management import CommandError
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause until database is ready.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Maximum number of seconds to wait for the database.",
        )

    def handle(self, *args, **options):
        timeout_seconds = options["timeout"]
        elapsed_seconds = 0

        self.stdout.write("\nWaiting for database...")
        while True:
            try:
                connections["default"].ensure_connection()
                break
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                elapsed_seconds += 1

                if elapsed_seconds >= timeout_seconds:
                    self.stdout.write(self.style.ERROR("Database did not become available within the specified timeout."))
                    raise CommandError(
                        f"Timeout: Database unavailable after {elapsed_seconds} seconds."
                    )
                
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available."))
