from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateField()
    body = models.TextField()

class Subject(models.Model):
    name = models.CharField(max_length=200)
    professor = models.CharField(max_length=100)
    score = models.IntegerField()
    grade = models.CharField(max_length=2)
    review = models.TextField()