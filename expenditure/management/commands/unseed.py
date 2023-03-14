from django.core.management.base import BaseCommand, CommandError

from expenditure.models import User


class Command(BaseCommand):
    help = 'Unseeds the database with sample data'

    def handle(self, *args, **options):
        """Unseeds all users who are not staff"""
        User.objects.filter(is_staff=False).delete()
        self.stdout.write(self.style.SUCCESS('Users unseeded'))
