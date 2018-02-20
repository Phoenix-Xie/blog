from django.db import models
from login_and_sign.models import User
from . import setting
# Create your models here.


class Passage(models.Model):
    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'

    def __str__(self):
        return self.title
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', to_field='username')
    title = models.CharField(max_length=setting.Passage_title_max_length, verbose_name='标题')
    text = models.CharField(max_length=setting.Passage_text_max_length, verbose_name='文章内容')
    pub_time = models.DateTimeField(verbose_name='发表时间')
    type1 = models.CharField(max_length=setting.Passage_type1_max_length, default='无', verbose_name='标签1')
    type2 = models.CharField(max_length=setting.Passage_type2_max_length, default='无', verbose_name='标签2')
    type3 = models.CharField(max_length=setting.Passage_type3_max_length, default='无', verbose_name='标签3')
    # 向外关联一个User类进来作为该user的外键，并以username表示


class Comment(models.Model):
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.text[0:5]
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, verbose_name='所属文章')
    text = models.CharField(max_length=setting.Comment_text_max_length, verbose_name='评论内容')
    pub_time = models.DateTimeField(verbose_name='发表时间')

