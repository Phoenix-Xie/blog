from . import setting


def passage_test(title='1', text='1', type1='', type2='', type3=''):
    context = {'error_message': []}
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