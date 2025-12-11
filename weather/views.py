from datetime import date
import json

from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import City, Forecast
from .services import fetch_and_store_forecast, get_hourly_forecast


class ForecastView(View):
    template_name = "forecast.html"

    def get(self, request):

        # Kaikki kaupungit
        cities = City.objects.all().order_by("name")

        # Hakee kaupungin tiedot
        city_id = request.GET.get("city") or (cities.first().id if cities else None)
        city = get_object_or_404(City, id=city_id) if city_id else None

        # Päiväkohtainen ennuste
        if city:
            fetch_and_store_forecast(city)

        # Päivittäiset ennusteet 7 päivälle
        qs = (
            Forecast.objects
            .filter(city=city, date__gte=date.today())
            .order_by("date")[:7]
        ) if city else []

        labels    = [f.date.isoformat() for f in qs]
        data_max  = [float(f.temp_max) for f in qs]
        data_min  = [float(f.temp_min) for f in qs]
        data_rain = [float(f.rain_probability or 0) for f in qs]
        data_wind = [float(f.wind_speed or 0) for f in qs]
        data_code = [int(f.weather_code or 0) for f in qs]

        # Hakee tuntikohtaisen sääennusteen seuraavalle 7 päivälle.
        hourly = get_hourly_forecast(city) if city else {}
        hourly_json = json.dumps(hourly)

        ctx = {
            "cities": cities,
            "city": city,
            "forecasts": qs,      
            "labels": labels,
            "data_max": data_max,
            "data_min": data_min,
            "data_rain": data_rain,
            "data_wind": data_wind,
            "data_code": data_code,
            "hourly_json": hourly_json,
        }

        return render(request, self.template_name, ctx)
