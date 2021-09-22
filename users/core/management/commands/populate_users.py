from django.core.management import BaseCommand
from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.using('old').all()

        for user in users:
            User.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password,
                is_ambassador=user.is_ambassador
            )
