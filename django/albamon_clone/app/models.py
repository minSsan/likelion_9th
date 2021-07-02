from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=200)
    job_area = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    wage = models.IntegerField()
    job = models.TextField()
    applicant = models.IntegerField()

class Review(models.Model):
    user = models.CharField(max_length=200)
    current_store = models.ForeignKey(Store, on_delete=CASCADE, null=True)
    content = models.TextField()
    image = models.ImageField()
    pub_date = models.DateTimeField()