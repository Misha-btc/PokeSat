from django.core.management.base import BaseCommand
from sat_list.models import Transaction

class Command(BaseCommand):
    help = 'Clears the specified table'

    def handle(self, *args, **kwargs):
        Transaction.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared table'))
