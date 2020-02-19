import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
from users.models import User


# python manage.py hoon --times 50


class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        # users = User.objects.filter(first_name__startswith="c")
        users = User.objects.all()
        room_types = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        houseRules = HouseRule.objects.all()

        seeder.add_entity(
            Room,
            number,
            {
                # "country": "KR",
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(0, 20),
                "price": lambda x: random.randint(40000, 60000),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )
        create_photos = seeder.execute()
        create_clead = flatten(list(create_photos.values()))

        for pk in create_clead:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(13, 17)):

                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"/room_photos/{random.randint(1,31)}.webp",
                    room=room,
                )

            for a in amenities:
                magic_number = random.randint(0, 12)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 5)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in houseRules:
                magic_number = random.randint(0, 5)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"CREATE Rooms count : {number}"))
