import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users.models import User
from rooms.models import Room

# python manage.py hoon --times 50


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many reviews you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            Review,
            number,
            {
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE Reviews count : {number}"))
