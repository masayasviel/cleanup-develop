from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata


class Command(BaseCommand):
    help = 'dependency_load_fixture'

    def handle(self, *args, **options):
        management.call_command(loaddata.Command(), "user", verbosity=0)