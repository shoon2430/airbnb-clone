import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from users.models import User
from rooms.models import Room

# python manage.py hoon --times 50


NAME = "Reservation"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            Reservation,
            number,
            {
                "status": lambda x: random.choice(
                    ["pending", "comfirmed", "canceled",]
                ),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE {NAME} count : {number}"))
