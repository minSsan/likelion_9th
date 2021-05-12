from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Blog) # admin 사이트에 Blog table 등록
admin.site.register(Subject)