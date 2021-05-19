from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=200)
    job_area = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    wage = models.IntegerField()
    job = models.TextField()
    applicant = models.IntegerField()