from . import setting
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def passage_test(title='1', text='1', type1='', type2='', type3=''):
    context = {
                'error_message': [],
               'title': title,
               'text': text,
               'type1': type1,
               'type2': type2,
               'type3': type3,
               }
    if title == '' or title is None:
        context['error_message'].append('标题不能为空')
    if len(title) > setting.Passage_title_max_length:
        context['error_message'].append('标题长度不能超过'+str(setting.Passage_title_max_length))
    if text == '' or text is None:
        context['error_message'].append('文章内容不能为空')
    if len(text) > setting.Passage_text_max_length:
        context['error_message'].append('文章内容不能超过'+str(setting.Passage_text_max_length))
    if len(type1) > setting.Passage_type1_max_length:
        context['error_message'].append('类别1的长度不能超过'+str(setting.Passage_type1_max_length))
    if len(type2) > setting.Passage_type2_max_length:
        context['error_message'].append('类别2的长度不能超过'+str(setting.Passage_type1_max_length))
    if len(type3) > setting.Passage_type2_max_length:
        context['error_message'].append('类别3的长度不能超过' + str(setting.Passage_type1_max_length))
    return context


# 检测是否登入，登入返回username，未登入返回false
def test_login(request):
    try:
        username = request.session['username']
    except:
        return False
    return username


# 返回相应的文章列表，页码, 总页数
def objects_list(request, p_objects, page_items=setting.the_number_of_items_in_each_page):
    p = Paginator(p_objects, page_items)
    index = page_turning(request)
    context = {}
    try:
        context['passages'] = p.page(index)
    except PageNotAnInteger:
        index = 1
        context['passages'] = p.page(1)
    except EmptyPage:
        if index <= 0:
            index = 1
            context['passages'] = p.page(1)
            context['page_error'] = "已经到首页了"
        else:
            index = p.num_pages
            context['passages'] = p.page(p.num_pages)
            context['page_error'] = '已经到末页了'
    context['index'] = str(index)
    context['index_all'] = str(p.num_pages)
    return context


# 判断翻页函数，配合上一个函数使用吗，与page_turning.html共同使用
def page_turning(request):
    index = 1
    if request.method == 'GET':
        index = request.GET.get('index')
        if type(index) != int:
            index = 1
        if index is None:
            index = 1
        else:
            index = int(index)
        # 翻页
        if not request.GET.get('next_page', default=None) is None:
            index += 1
        if not request.GET.get('up_page', default=None) is None:
            index -= 1
    return index


