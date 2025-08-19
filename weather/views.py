from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import City, Forecast
from .services import fetch_and_store_forecast

class ForecastView(View):
    template_name = "forecast.html"

    def get(self, request):
        cities = City.objects.all().order_by('name')
        # Valitse oletuksena eka kaupunki
        city_id = request.GET.get("city") or (cities.first().id if cities else None)
        city = get_object_or_404(City, id=city_id) if city_id else None

        # Päivitä data aina GETissä:
        if city:
            fetch_and_store_forecast(city)

        qs = Forecast.objects.filter(city=city)[:7] if city else []
        labels = [f.date.isoformat() for f in qs]
        data_max = [float(f.temp_max) for f in qs]
        data_min = [float(f.temp_min) for f in qs]

        ctx = {
            "cities": cities,
            "city": city,
            "labels": labels,
            "data_max": data_max,
            "data_min": data_min,
        }
        return render(request, self.template_name, ctx)
