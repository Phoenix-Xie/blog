from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from blogs.models import Passage
from login_and_sign.models import User
import time
# Create your views here.


def home(request):
    page_item = 5
    passage_pages = int(Passage.objects.count()/page_item) + 1
    try:
        index = request.session.get('index', default=1)
        print("123")
    except Exception:
        context = {}
        context['error_message'] = ['页码获取出错']
        return render(request, 'blog/error.html', context)
    # if request.POST.get('')
    try:
        username = request.session.get('username', default=None)
    except Exception:
        context = {}
        context['error_message'] = ['用户名获取出错']
        return render(request, 'blog/error.html', context)
    if username is None:
        context = {}
        context['error_message'] = ['用户名获取出错']
        return render(request, 'blog/error.html', context)
    context = {}
    if request.method == 'GET':
        next_page = request.GET.get('next_page')
        up_page = request.GET.get('up_page')
        if not request.GET.get('new_passage') is None:
            return HttpResponseRedirect(reverse('blogs:add_passage'))
        if not request.GET.get('exit') is None:
            return render(request, 'blog/logout.html')
        if not request.GET.get('next_page', default=None) is None:
            index += 1
        if not request.GET.get('up_page', default=None) is None:
            index -= 1
        if index == 0:
            context['error_message'] = "<script>alert('已经到首页了')</script>"
            index = 1
        if index == passage_pages+1:
            context['error_message'] = '<script>alert("已经到末页了")</script>'
            index = passage_pages

    if username is None:
        context['error_message'] = '请先登入'
        return render(request, 'login_and_sign/login.html', context)
    context['username'] = username
    context['index'] = index
    context['index_all'] = passage_pages
    print(passage_pages, '   ', index)
    try:
        passage_list = Passage.objects.all()[page_item*(index-1): page_item*index].values('title', 'id', 'pub_time')
    except:
        context['error_message'] = '页码错误'
        return render(request, 'blog/error.html', context)
    context['passages'] = passage_list
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
        username = request.session.get("username")
    except Exception as e:
        context = {'error_message': '请先登入'}
        return render(request, 'login_and_sign/login.html', context)
    if username is None:
        context = {'error_message': '请先登入'}
        return render(request, 'login_and_sign/login.html', context)
    user = User.objects.get(username=username)
    passages = Passage.objects.filter(username_id=user.id).values('id', 'title', 'pub_time')
    context = {}
    context['passages'] = passages
    context['username'] = username
    return render(request, 'blog/self_home.html', context)


def passage_edit(request, passage_id):
    print(passage_id)
    try:
        p = Passage.objects.get(id=passage_id)
    except Exception as e:
        context = {}
        context['error_message'] = ['未找到相应文章,可能是该文章已删除']
        return render(request, 'blog/error.html', context)
    if not request.GET.get('delete') is None:
        try:
            p.delete()
        except:
            context = {}
            context['error_message'] = ['文章删除失败']
            return render(request, 'blog/error.html', context)
        context = {'message': '删除成功'}
        return render(request, 'blog/edit_statu.html', context)
    context = {}
    context['text'] = p.text
    context['title'] = p.title
    context['pub_time'] = p.pub_time
    context['passage_id'] = p.id
    return render(request, 'blog/passage_edit.html', context)


def edit_statu(request, passage_id):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', default=None)
            title = request.POST.get('title', default=None)
        except:
            context = {}
            context['error_message'] = ['修改出现错误']
            return render(request, 'blog/error.html', context)
        context = {}
        message = []
        if text is None or text == '':
            message.append('文章内容不能为空')
        if title is None or title == '':
            message.append('标题不能为空')
        if not message:
            message.append('成功修改')
            p = Passage.objects.get(id=passage_id)
            p.title = title
            p.text = text
            p.save()
        context['message'] = message
        return render(request, 'blog/edit_statu.html', context)


def add_passage(request):
    return render(request, 'blog/add_passage.html')


def add_statu(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            text = request.POST.get('passage')
            type1 = request.POST.get('type1')
            type2 = request.POST.get('type2')
            type3 = request.POST.get('type3')
            username = request.session.get('username')
            if username is None:
                context = {'error_message': '请先登录'}
                return render(request, 'login_and_sign/login.html', context)
        except:
            context = {'error_message': '标题和文章获取失败'}
            return render(request, 'blog/error.html', context)
        error_count = 0
        context = {'error_message': []}
        if title == '':
            error_count += 1
            context['error_message'].append('标题不能为空')
        if text == '':
            error_count += 1
            context['error_message'].append('内容不能为空')
        if error_count != 0:
            return render(request, 'blog/add_passage.html', context)
        user_id = User.objects.get(username=username).id
        pub_time = time.strftime("%Y-%m-%d", time.localtime())
        p = Passage(pub_time=pub_time, username_id=user_id, title=title, text=text, type1=type1, type2=type2, type3=type3)
        p.save()
        return HttpResponseRedirect(reverse('blogs:home'))
    else:
        context = {'error_message': '请以正常渠道进入，谢谢合作' }
        return render(request, 'blog/error.html', context)


def search(request):
    if request.method == 'GET':
        try:
            search_text = request.GET.get('search_text')
            search_result = Passage.objects.filter(title__contains=search_text)
            search_result.order_by('pub_time')
        except:
            context = {'error_message': '搜索失败'}
            return render(request, 'blog/error.html', context)
        passages = search_result.values('id', 'title', 'pub_time')
        context = {'passages': passages}
        return render(request, 'blog/search_result.html', context)
    context = {'error_message': '请以正常形式登入搜索'}
    return render(request, 'blog/error.html', context)
