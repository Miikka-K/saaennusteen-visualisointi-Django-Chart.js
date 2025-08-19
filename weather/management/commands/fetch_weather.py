from django.core.management.base import BaseCommand
from weather.models import City
from weather.services import fetch_and_store_forecast

class Command(BaseCommand):
    help = "Fetches and stores forecast data for all cities"

    def handle(self, *args, **options):
        for city in City.objects.all():
            self.stdout.write(f"Fetching {city}…")
            fetch_and_store_forecast(city)
        self.stdout.write(self.style.SUCCESS("Done."))
