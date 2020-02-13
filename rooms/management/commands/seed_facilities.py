from django.core.management.base import BaseCommand
from rooms import models as rooms_models


# python manage.py hoon --times 50


class Command(BaseCommand):

    help = "This command creates facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        count_facilities = len(facilities)

        for facilities in facilities:
            rooms_models.Facility.objects.create(name=facilities)

        self.stdout.write(
            self.style.SUCCESS(f"CREATE facilities - count : {count_facilities}")
        )

