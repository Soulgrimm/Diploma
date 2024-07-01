from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='84444444444',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('qqqwww111222')
        user.save()
