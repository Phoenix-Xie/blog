from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from blogs.models import Passage, Comment
from login_and_sign.models import User
from . import setting, func
import time, re
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def home(request):
    index = 1
    # 检测登入
    username = func.test_login(request)
    if not username:
        return render(request, 'login_and_sign/login.html', {'error_message': '请先登入'})
    context = {}

    if request.method == 'GET':
        # 新增passage
        if not request.GET.get('new_passage') is None:
            return HttpResponseRedirect(reverse('blogs:add_passage'))
        # 退出
        if not request.GET.get('exit') is None:
            del request.session['username']
            return HttpResponseRedirect(reverse('login'))
        if not request.GET.get('change_password') is None:
            return render(request, 'blog/change_password.html')
        index = func.page_turning(request)

    p = Passage.objects.all()
    context = func.objects_list(request, p)
    context['username'] = username
    return render(request, 'blog/home.html', context)


def passage_detail(request, passage_id):
    if request.method == 'GET':
        if request.GET.get('delete') == '删除':
            comment_id = request.GET.get('comment_id')
            c = Comment.objects.get(id=comment_id)
            c.delete()
            return HttpResponseRedirect(reverse('blogs:passage_detail', args=(passage_id, )))
    username = func.test_login(request)
    if not username:
        return render(request, 'login_and_sign/login.html')
    p = Passage.objects.get(id=passage_id)
    c = Comment.objects.filter(passage_id=passage_id).values('id', 'text', 'username_id__username', 'pub_time')
    context = {'title': p.title,
               'text': p.text,
               'pub_time': p.pub_time,
               'username': p.username_id.username,
               'type1': p.type1,
               'type2': p.type2,
               'type3': p.type3,
               'passage_id': passage_id,
               'comment': c
               }
    if username == p.username_id.username:
        context['delete'] = 'delete'
    return render(request, 'blog/passage_detail.html', context)


def self_home(request):
    # 检测登入
    username = func.test_login(request)
    if not username:
        return render(request, 'login_and_sign/login.html', {'error_message': '请先登入'})

    user = User.objects.get(username=username)
    passages = Passage.objects.filter(username_id=user.id).values('id', 'title', 'pub_time')
    context = func.objects_list(request, passages)
    context['username'] = username
    return render(request, 'blog/self_home.html', context)


def passage_edit(request, passage_id):
    try:
        p = Passage.objects.get(id=passage_id)
    except Exception as e:
        context = {}
        context['error_message'] = ['未找到相应文章,可能是该文章已删除']
        return render(request, 'blog/error.html', context)
    if request.GET.get('visit') == '访问该文章':
        return HttpResponseRedirect(reverse('blogs:passage_detail', args=(passage_id,)))
    if not request.GET.get('delete') is None:
        try:
            p.delete()
        except:
            context = {}
            context['error_message'] = ['文章删除失败']
            return render(request, 'blog/error.html', context)
        context = {'error_message': ['删除成功', ]}
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
        context = func.passage_test(title=title, text=text)
        if context['error_message'] != []:
            return render(request, 'blog/edit_statu.html', context)
        p = Passage.objects.get(id=passage_id)
        p.title = title
        p.text = text
        p.save()
        context['error_message'] = ['修改成功', ]
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
        context = func.passage_test(title, text, type1, type2, type3)
        if context['error_message'] != []:
            return render(request, 'blog/add_passage.html', context)
        user = User.objects.get(username=username)
        pub_time = time.strftime("%Y-%m-%d", time.localtime())
        p = Passage(pub_time=pub_time,
                    username_id=user,
                    title=title,
                    text=text,
                    type1=type1,
                    type2=type2,
                    type3=type3)
        p.save()
        return HttpResponseRedirect(reverse('blogs:home'))
    else:
        context = {'error_message': '请以正常渠道进入，谢谢合作' }
        return render(request, 'blog/error.html', context)


def search(request):
    try:
        search_text = request.GET.get('search_text')
        search_type = request.GET.get('search_type')
        if search_text is None:
            search_text = ''
        if search_type == 'title':
            search_result = Passage.objects.filter(title__contains=search_text)
        elif search_type == 'text':
            search_result = Passage.objects.filter(text__contains=search_text)
        elif search_type == 'username':
            search_result = Passage.objects.filter(username_id__username__contains=search_text)
        else:
            search_result = Passage.objects.filter(Q(type1__contains=search_text)
                                                   | Q(type2__contains=search_text)
                                                   | Q(type3__contains=search_text))
        search_result.order_by('pub_time')
    except:
        context = {'error_message': '搜索失败'}
        return render(request, 'blog/error.html', context)
    context = func.objects_list(request, search_result)
    return render(request, 'blog/search_result.html', context)


def add_comment(request, passage_id):
    context = {'passage_id': passage_id}
    return render(request, 'blog/add_comment.html', context)


def add_comment_statu(request, passage_id):
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
        except:
            context = {'error_message': '评论发送失败'}
            return render(request, 'blog/error.html', context)
        try:
            username = request.session.get('username')
            user = User.objects.get(username=username)
        except:
            context = {'error_message': '请先登入'}
            return render(request, 'login_and_sign/login.html', context)
        if text == '':
            context = {'error_message': '文章内容不能为空', 'text':text}
            return render(request, 'blog/add_comment.html', context)
        if len(text) > setting.Comment_text_max_length:
            context = {'error_message': '文章内容不能超过'+str(setting.Comment_text_max_length), 'text':text}
            return render(request, 'blog/add_comment.html', context)
        passage = Passage.objects.get(id=passage_id)
        comment = Comment(text=text,
                          username_id=user,
                          pub_time=time.strftime("%Y-%m-%d", time.localtime()),
                          passage_id=passage,
                          )
        comment.save()
        return HttpResponseRedirect(reverse('blogs:passage_detail', args=(passage_id,)))


def change_password(request):
    username = func.test_login(request)
    if not username:
        return render(request, 'login_and_sign/login.html', {'error_message': '请先登入'})

    try:
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
    except:
        return render(request, 'blog/error.html', {'error_message': '获取错误'})

    user = User.objects.get(username=username)
    error_counter = 0
    error_list = []
    if not check_password(old_password, user.password):
        return render(request, 'blog/error.html', {'error_message': '密码错误'})
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

    if error_counter:
        context = {'error_message': '密码修改失败', 'error_list': error_list}
        return render(request, 'blog/change_password.html', context)
    else:
        user.password = make_password(password)
        user.save()
        context = {'error_message': ['密码修改成功', ]}
        return render(request, 'blog/error.html', context)




