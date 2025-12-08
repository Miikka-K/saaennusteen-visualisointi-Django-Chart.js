import requests
from datetime import datetime, date, timedelta
from .models import Forecast, City

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_and_store_forecast(city: City):
    today = date.today()
    end_date = today + timedelta(days=6)

    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "start_date": today.isoformat(),
        "end_date": end_date.isoformat(),
    }

    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=20)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API-yhteys epäonnistui: {e}")
        return

    data = r.json()
    dates = data.get("daily", {}).get("time", [])
    maxes = data.get("daily", {}).get("temperature_2m_max", [])
    mins  = data.get("daily", {}).get("temperature_2m_min", [])

    for d, tmax, tmin in zip(dates, maxes, mins):
        Forecast.objects.update_or_create(
            city=city,
            date=datetime.fromisoformat(d).date(),
            defaults={"temp_max": tmax, "temp_min": tmin},
        )
