from django.shortcuts import redirect, render
from django.http import request
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
# AuthenticationForm : 로그인을 가능하게 해주는 폼
# UserCreationForm : 회원가입을 가능하게 해주는 폼

def main(request):
    return render(request, "main.html")

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
            return redirect('main')
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
    return redirect('main')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # 유저 정보를 USER DB에 저장
            login(request, user) # 유저를 로그인 상태로 변경
        return redirect('main')
    else:    
        form = UserCreationForm()
        return render(request, 'signup.html', {'form':form})