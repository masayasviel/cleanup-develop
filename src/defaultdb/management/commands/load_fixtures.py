from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'dependency_load_fixture'

    def handle(self, *args, **options):
        print('Hello World!')