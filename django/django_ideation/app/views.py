from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    members = Member.objects.all()
    return render(request, 'home.html', {'members': members})