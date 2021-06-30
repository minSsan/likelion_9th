from django.db import models

class Medical(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Detail(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)