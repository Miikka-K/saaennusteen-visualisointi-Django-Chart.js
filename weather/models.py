from django.db import models

class City(models.Model):
    name = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='forecasts')
    date = models.DateField()
    temp_max = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)

    rain_probability = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)

    weather_code = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('city', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.city} {self.date}"
