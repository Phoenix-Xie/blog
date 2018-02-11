from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from blogs.models import Passage
# Create your views here.


def home(request):
    if request.method == 'POST':
        try:
            index = request.session.get('index', default=None)
        except Exception:
            context = {}
            context['error_message'] = ['页码获取出错']
            return render(request, 'blog/error.html', context)
        #if request.POST.get('')
    try:
        username = request.session.get('username', default=None)

    except Exception:
        context = {}
        context['error_message'] = ['用户名获取出错']
        return render(request, 'blog/error.html', context)
    context = {}
    if index == None:
        index = 1;
    if username is None:
        context['errormessage'] = '请先登入'
        return render(request, 'login_and_sign/login.html', context)
    context['username'] = username
    context['index'] = index
    passage_list = Passage.objects.order_by('pub_time')[5*(index-1): 5*index]
    return render(request, 'blog/home.html', context)


def passage_detail(request, passage_id):
    p = Passage.objects.get(id=passage_id)
    context = {'title': p.title,
               'text': p.text,
               'pub_time': p.pub_time,
               'username': p.username,
               'type1': p.type1,
               'type2': p.type2,
               'type3': p.type3,
               }
    return render(request, 'blog/passage_detail.html', context)


def self_home(request):
    try:
        username = request.session.get("usename")
    except Exception as e:
        context = {'errormessage': '请先登入'}
        return render(request, 'login_and_sign/login.html', context)
    passage = Passage.objects.filter(username=username)
    context = {}
    for p in passage:
        context[p.id] = (p.title, p.pub_time, p.id)
    return render(request, 'blog/self_home.html', context)


def passage_edit(request, passage_id):
    try:
        p = Passage.objects.get(passage_id = passage_id)
    except Exception as e:
        context = {}
        context['error_message'] = ['未找到相应文章,可能是该文章已删除']
        return render(request, 'blog/error.html', context)
    context = {}
    context['text'] = p.text
    context['title'] = p.title
    context['pub_time'] = p.pub_time
    return render(request, '')


def edit_statu(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', default=None)
            title = request.POST.get('title', default=None)
        except:
            context = {}
            context['error_message'] = ['修改出现错误']
            return render(request, 'blog/error.html', context)
        context = {}
        errormessage = []
        if text is None:
            errormessage.append('文章内容不能为空')
        if title is None:
            errormessage.append('标题不能为空')
        context['error_message'] = errormessage
        return render(request, 'blog/edit_statu.html', context)
