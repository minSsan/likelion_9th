from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import *

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    context = {
        "blogs" : blogs
    }
    return render(request, 'home.html', context)

def detail(request, id):
    detail_data = get_object_or_404(Blog, pk=id)
    # pk: primary key(특정 정보에 관련된 정보들만 추출하기 위해 사용)
    context = {
        "title" : detail_data.title,
        "writer" : detail_data.writer,
        "body" : detail_data.body,
        "pub_date" : detail_data.pub_date,
        "id" : id,
    }
    return render(request, 'detail.html', context)

def create_page(request):
    return render(request, 'create.html')

def create(request):
    new_data = Blog()
    new_data.title = request.POST['title']
    new_data.writer = request.POST['writer']
    new_data.body = request.POST['body']
    new_data.pub_date = timezone.now()
    new_data.save()
    return redirect('home')
    # redirect: 특정 url을 실행시킴

def update_page(request, id):
    update_data = get_object_or_404(Blog, pk=id)
    context = {
        'id': id,
        'title' : update_data.title,
        'writer' : update_data.writer,
        'body' : update_data.body,
    }
    return render(request, 'update.html', context)

def update(request, id):
    update_data = get_object_or_404(Blog, pk=id)
    update_data.title = request.POST['title']
    update_data.writer = request.POST['writer']
    update_data.body = request.POST['body']
    update_data.pub_date = timezone.now()
    update_data.save()
    return redirect('home')

def delete(request, id):
    delete_data = get_object_or_404(Blog, pk=id)
    delete_data.delete()
    return redirect('home')