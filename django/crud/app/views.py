from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator

from .models import *

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    # blogs를 한 페이지에 6개씩 담을 것이다
    page = request.GET.get('page')
    # 사용자가 현재 보고 있는 페이지의 번호를 저장
    posts = paginator.get_page(page)
    # 사용자가 현재 보고 있는 페이지를 저장
    # 즉, posts는 최대 총 5개의 블로그 객체를 담고 있음

    context = {
        "blogs" : blogs,
        "posts" : posts,
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == "POST": # request가 POST인 경우
        # 사용자가 로그인 화면에서 정보를 입력하고 버튼을 누를 때는 POST 방식으로 login_view를 호출
        # -> 로그인 상태로 변경하는 로직
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid(): # 유효성 검사
            username = form.cleaned_data.get('username')
            # form.cleaned_data: 유효성 검사를 통과한 데이터를 의미
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username = username, password = password)
            # authenticate: 유저 인증 함수
            if user is not None: # 유저가 인증된 상태 즉, 입력 정보가 가입된 유저라면
                login(request, user) # 유저를 로그인 상태로 바꿈
        return redirect('home')
    else: # request가 Get인 경우
        # 메인 화면에서 로그인 버튼을 누를 때 GET 방식으로 login_view 호출
        # -> 이 경우에 login.html을 렌더링
        form = AuthenticationForm()
        context = {
            'form':form,
        }
        return render(request, "login.html", context) # 렌더링: Get 방식

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # 유저 정보를 USER DB에 저장
            login(request, user) # 유저를 로그인 상태로 변경
        return redirect('home')
    else:    
        form = UserCreationForm()
        return render(request, 'signup.html', {'form':form})

def detail(request, id):
    detail_data = get_object_or_404(Blog, pk=id)
    # pk: primary key(특정 정보에 관련된 정보들만 추출하기 위해 사용)
    comments = Comment.objects.filter(blog_id = id)
    # blog_id -> 특정 글의 댓글만 추출하기 위해 사용
    # blog_id 라는 변수의 값이 id인 Comment 객체만 불러오겠다
    context = {
        "title" : detail_data.title,
        "writer" : detail_data.writer,
        "body" : detail_data.body,
        "pub_date" : detail_data.pub_date,
        "id" : id,
        'comments': comments,
        'image':detail_data.image,
    }
    return render(request, 'detail.html', context)

def create_page(request):
    return render(request, 'create.html')

def create(request):
    new_data = Blog()
    new_data.title = request.POST['title']
    new_data.writer = request.POST['writer']
    new_data.body = request.POST['body']
    new_data.image = request.FILES['image']
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
        'image' : update_data.image,
    }
    return render(request, 'update.html', context)

def update(request, id):
    update_data = get_object_or_404(Blog, pk=id)
    update_data.title = request.POST['title']
    update_data.writer = request.POST['writer']
    update_data.body = request.POST['body']
    update_data.image = request.FILES['image']
    update_data.pub_date = timezone.now()
    update_data.save()
    return redirect('home')

def delete(request, id):
    delete_data = get_object_or_404(Blog, pk=id)
    delete_data.delete()
    return redirect('home')

def create_comment(request, id):
    new_comment = Comment()
    blog_id = Blog.objects.get(pk=id)
    new_comment.blog_id = blog_id
    new_comment.user = request.POST['user']
    new_comment.content = request.POST['content']
    new_comment.date = timezone.now()
    new_comment.save() 
    return redirect('detail', id)

def delete_comment(request, id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('detail', id)