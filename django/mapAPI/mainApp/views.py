from django.shortcuts import render
from .models import Cafe

# Create your views here.
def main(request):
    cafes = Cafe.objects.all()
    context = {
        'cafes':cafes,
    }
    return render(request, 'main.html', context)