from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    major = models.CharField(max_length = 100)
    mbti = models.CharField(max_length = 5)
    introduce = models.TextField()