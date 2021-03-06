from django.shortcuts import render
from django import forms
import re
from django.http import HttpResponseRedirect, HttpResponse, Http404
from io import BytesIO
from .models import User
from django.urls import reverse
from . import setting, func
import random
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
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
        if not request.POST.get('forget') is None:
            username = request.POST.get('username')
            try:
                user = User.objects.get(username=username)
            except:
                context = {'error_message': '请填入正确用户名后找回密码', 'username': username}
                return render(request, "login_and_sign/login.html", context)
            reset_password = ''.join(random.sample(setting.chars_for_reset_password, setting.the_length_of_reset_password))
            reset_password_deal = make_password(reset_password)
            net = setting.base_website_location_for_reset_password+reset_password_deal+'/verify?username='+username+'&reset_password='+reset_password
            message = net + '    访问该网址完成密码重置'
            send_mail('重置密码', message, 'easyblog <easyblog123@163.com>', [user.email, ], fail_silently=False)
            context = {
                'message': '验证已发送至邮箱,请登入邮箱验证',
                'title': '重置密码',
            }
            return render(request, 'login_and_sign/errors.html', context)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not func.check_code(request):
            context = {'error_message': '验证码错误，请重新登入', 'username': username}
            return render(request, "login_and_sign/login.html", context)
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            context = {'error_message': '用户名或密码错误，登录失败，请重新登入', 'username': username}
            return render(request, "login_and_sign/login.html", context)
        else:
            if check_password(password, user.password):
                request.session['username'] = username
                return HttpResponseRedirect(reverse('blogs:home'))
            else:
                context = {'error_message': '用户名或密码错误，登录失败，请重新登入', 'username': username}
                return render(request, "login_and_sign/login.html", context)


def sign(request):
    # print("third") #test
    return render(request, "login_and_sign/sign.html")


def sign_message(request):
    # 原本使用POST['']来获取，但如果未获取不能返回默认值，因而改成get，默认无返回None 可加参数default修改
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    username = request.POST.get('username')
    email = request.POST.get('email')
    error_list = []
    error_counter = 0
    if not func.check_code(request):
        error_counter += 1
        error_list.append(str(error_counter) + '.验证码错误')
    if username == '':
        error_counter += 1
        error_list.append(str(error_counter)+'.用户名不能为空')
    if User.objects.filter(username=username).count() != 0:
        error_counter += 1
        error_list.append(str(error_counter) + '.用户名已被注册')
    if len(username) > setting.the_largest_length_of_username:
        error_counter += 1
        error_list.append(str(error_counter) + '.用户名超过' + str(setting.the_largest_length_of_username))
    if password != password2:
        error_counter += 1
        error_list.append(str(error_counter) + '.两次输入密码不符')
    if len(password) < setting.the_least_length_of_password:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码过短，需要至少'+str(setting.the_least_length_of_password)+'位密码')
    if len(password) > setting.the_largest_length_of_password_for_user:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码过长，最多为' + str(setting.the_least_length_of_password) + '位密码')
    if re.search(r'[0-9]', password) is None:
        error_counter += 1
        error_list.append(str(error_counter) + '.密码中必须含有数字')
    if (re.search(r'[a-z]+', password) is None) and (re.search(r'[A-Z]+', password) is None):
        error_counter += 1
        error_list.append(str(error_counter) + '.密码中必须含有字母(大小写皆可)')
    if len(email) > setting.the_largest_length_of_email:
        error_counter += 1
        error_list.append(str(error_counter) + '.邮箱过长,应小于'+str(setting.the_largest_length_of_email)+'位')
    # 检测是否与邮箱近似
    # r'\w{1,12}@(qq.com|163.com)
    parttem = r'\w{1,12}@('
    length = len(setting.the_email_can_be_use)
    c = 0
    for i in setting.the_email_can_be_use:
        c += 1
        if length == c:
            parttem += i
        else:
            parttem += (i+'|')
    parttem += ')'
    if re.match(parttem, email) is None:
        error_counter += 1
        email_can_be_use = ''
        for i in setting.the_email_can_be_use:
            email_can_be_use += i+','
        error_list.append(str(error_counter)+'.邮箱不正确，必须使用'+email_can_be_use+'邮箱结尾')
    if error_counter != 0:
        context = {"error_list": error_list,
                   "message": "注册失败,错误信息如下",
                   'username': username,
                   'email': email,
                   'title': '注册情况',
                   }
        return render(request, 'login_and_sign/sign.html', context)
    else:
        context = {"message": "注册成功"}
        password = make_password(password)
        user = User(username=username, password=password, email=email)
        user.save()
        return render(request, 'login_and_sign/errors.html', context)


def create_code_img(request):
    f = BytesIO()
    savepath = 'D:\image'
    img, code = func.create_validate_code()
    request.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


def verify(request, password_verify):
    try:
        reset_password = request.GET.get('reset_password')
        username = request.GET.get('username')
        user = User.objects.get(username=username)
    except:
        context = {
            'message': '密码重置失败',
            'title': '重置密码',
        }
        return render(request, 'login_and_sign/errors.html', context)
    if check_password(reset_password, password_verify):
        user.password = make_password(reset_password)
        user.save()
        context = {
            'message': '密码重置成功, 密码重置为 '+reset_password+',请小心保管',
            'title': '重置密码',
        }
        return render(request, 'login_and_sign/errors.html', context)
    else:
        context = {
            'message': '密码重置失败',
            'title': '重置密码',
        }
        return render(request, 'login_and_sign/errors.html', context)
