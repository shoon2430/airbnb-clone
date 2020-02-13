import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room

# python manage.py hoon --times 50

NAME = "List"


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
            List, number, {"user": lambda x: random.choice(users),},
        )

        create_lists = seeder.execute()
        create_clead = flatten(list(create_lists.values()))

        for pk in create_clead:
            pklist = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]

            # 쿼리셋안의 데이터를 가져옴  *
            # print("Q set : ", to_add)
            # print("set : ", *to_add)
            pklist.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"CREATE {NAME} count : {number}"))
