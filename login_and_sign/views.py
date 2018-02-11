from django.shortcuts import render, get_object_or_404
from django import forms
import re
from django.http import HttpResponseRedirect
from .models import User
import blogs
from django.contrib import messages
from django.urls import reverse
# Create your views here.


class UserForm(forms.Form):
    password = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    email = forms.CharField(max_length=20)


def login(request):
    return render(request, 'login_and_sign/login.html')


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            context = {'errormessage': '用户名或密码错误，登录失败，请重新登入'}
            return render(request, "login_and_sign/login.html", context)
        else:
            print(user.password)
            if user.password == password:
                request.session['username'] = username
                return HttpResponseRedirect(reverse('blogs:home'))
            else:
                context = {'errormessage': '用户名或密码错误，登录失败，请重新登入'}
                return render(request, "login_and_sign/login.html", context)


def sign(request):
    #print("third") #test
    return render(request, "login_and_sign/sign.html")


def sign_message(request):
    #原本使用POST['']来获取，但如果未获取不能返回默认值，因而改成get，默认无返回None 可加参数default修改
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    username = request.POST.get('username')
    email = request.POST.get('email')
    error_list = []
    error_counter = 0
    if User.objects.filter(username=username).count() == 0:
        error_counter += 1
        error_list.append(str(error_counter) + '.用户名已被注册')
    if password != password2:
        error_counter += 1
        error_list.append(str(error_counter) + '.两次输入密码不符')
    if len(password) < 5:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码过短，需要至少5位密码')
    if re.search(r'[0-9]', password) is None:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码中必须含有数字')
    if re.search(r'[a-z][A-Z]', password) is None:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码中必须含有字母(大小写皆可)')
    # 检测是否与邮箱近似
    if error_counter != 0:
        context = {"error_list": error_list, "message": "注册失败,错误信息如下"}
        return render(request, 'login_and_sign/errors.html', context)
    else:
        context = {"message": "注册成功"}
        user = User(username=username, password=password, email=email)
        user.save()
        return render(request, 'login_and_sign/errors.html', context)

    '''if request.method == 'POST':
        print("second")
        form = UserForm(request.POST)
        if form.is_valid():
            user = models.User()
            user.username = form.cleaned_data["username"]
            user.password = form.cleaned_data["password"]
            user.email = form.cleaned_data["email"]
            user.save()''' #使用form类型，未知是否可行