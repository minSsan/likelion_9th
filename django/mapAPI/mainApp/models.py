from django.db import models

class Cafe(models.Model):
    name = models.CharField(max_length=20)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)