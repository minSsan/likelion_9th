from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import *

# Create your views here.
def home(request):
    stores = Store.objects.all()
    context = {
        'stores':stores,
    }
    return render(request, 'home.html', context)

def create_page(request):
    return render(request, 'create_page.html')

def modify_page(request, id):
    this = get_object_or_404(Store, pk=id)
    context = {
        'name':this.name,
        'job_area':this.job_area,
        'detail':this.detail,
        'location':this.location,
        'wage':this.wage,
        'job':this.job,
        'id':id,
    }
    return render(request, 'modify_page.html' ,context)

def detail_page(request, id):
    this = get_object_or_404(Store, pk=id)
    context = {
        'name':this.name,
        'job_area':this.job_area,
        'detail':this.detail,
        'location':this.location,
        'wage':this.wage,
        'job':this.job,
        'applicant':this.applicant,
        'id':id,
    }
    return render(request, 'detail.html', context)

def increase_applicant(request, id):
    modify_data = get_object_or_404(Store, pk=id)
    modify_data.applicant += 1
    modify_data.save()
    return redirect('detail', id)

def decrease_applicant(request, id):
    modify_data = get_object_or_404(Store, pk=id)
    if(modify_data.applicant > 0):
        modify_data.applicant -= 1
    modify_data.save()
    return redirect('detail', id)

def upload(request):
    new_data = Store()
    new_data.name = request.POST['name']
    new_data.job_area = request.POST['job_area']
    new_data.detail = request.POST['detail']
    new_data.location = request.POST['location']
    new_data.wage = request.POST['wage']
    new_data.job = request.POST['job']
    new_data.applicant = 0
    new_data.save()
    return redirect('home')

def modify(request, id):
    modify_data = get_object_or_404(Store, pk=id)
    modify_data.name = request.POST['name']
    modify_data.job_area = request.POST['job_area']
    modify_data.detail = request.POST['detail']
    modify_data.location = request.POST['location']
    modify_data.wage = request.POST['wage']
    modify_data.job = request.POST['job']
    modify_data.applicant = modify_data.applicant
    modify_data.save()
    return redirect('detail', id)

def delete(request, id):
    delete_data = get_object_or_404(Store, pk=id)
    delete_data.delete()
    return redirect('home')

def upload_review(request, id):
    new_review = Review()
    new_review.current_store = Store.objects.get(pk=id)
    new_review.user = request.POST['user']
    new_review.content = request.POST['content']
    new_review.image = request.FILES['image']
    new_review.pub_date = timezone.now()
    new_review.save()
    return redirect('detail', id)