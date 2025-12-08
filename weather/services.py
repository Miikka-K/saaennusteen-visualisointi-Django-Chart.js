import requests
from datetime import date, timedelta, datetime
from collections import defaultdict

from .models import Forecast, City

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_and_store_forecast(city: City):
    today = date.today()
    end_date = today + timedelta(days=6)

    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "daily": (
            "weathercode,"                    # 👈 put weathercode first
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "windspeed_10m_max"
        ),
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
    daily = data.get("daily", {})

    print("daily keys from API:", daily.keys())          # 👈 debug
    codes = daily.get("weathercode", [])
    print("weather codes from API:", codes)              # 👈 debug

    dates = daily.get("time", [])
    maxes = daily.get("temperature_2m_max", [])
    mins  = daily.get("temperature_2m_min", [])
    rains = daily.get("precipitation_probability_max", [])
    winds = daily.get("windspeed_10m_max", [])

    for d, tmax, tmin, rain, wind, code in zip(dates, maxes, mins, rains, winds, codes):
        Forecast.objects.update_or_create(
            city=city,
            date=datetime.fromisoformat(d).date(),
            defaults={
                "temp_max": tmax,
                "temp_min": tmin,
                "rain_probability": rain,
                "wind_speed": wind,
                "weather_code": code,
            },
        )

def get_hourly_forecast(city: City):
    """
    Hakee tuntikohtaisen lämpötilan seuraaville 7 päivälle
    ja palauttaa rakenteen:
    {
        "2025-12-08": [{"time": "00:00", "temp": 5.1}, ...],
        "2025-12-09": [...],
        ...
    }
    """
    today = date.today()
    end_date = today + timedelta(days=6)

    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "hourly": "temperature_2m",
        "timezone": "auto",
        "start_date": today.isoformat(),
        "end_date": end_date.isoformat(),
    }

    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=20)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Hourly API request failed: {e}")
        return {}

    data = r.json()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    result = defaultdict(list)
    for t, temp in zip(times, temps):
        # t esimerkki: "2025-12-08T10:00"
        dt = datetime.fromisoformat(t)
        date_str = dt.date().isoformat()   # "2025-12-08"
        time_str = dt.strftime("%H:%M")    # "10:00"
        result[date_str].append({
            "time": time_str,
            "temp": temp,
        })

    return result