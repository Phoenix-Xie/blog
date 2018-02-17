from django.db import models
from login_and_sign.models import User
# Create your models here.


class Passage(models.Model):
    class Meta:
        verbose_name = '博客文'
        verbose_name_plural = '博客文'
    def __str__(self):
        return self.title
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    title = models.CharField(max_length=30, verbose_name='标题')
    text = models.CharField(max_length=2000, verbose_name='文章内容')
    pub_time = models.DateTimeField(verbose_name='发表时间')
    type1 = models.CharField(max_length=50, default='无', verbose_name='标签1')
    type2 = models.CharField(max_length=50, default='无', verbose_name='标签2')
    type3 = models.CharField(max_length=50, default='无', verbose_name='标签3')
    #向外关联一个User类进来作为该user的外键，并以username表示


class global_variable:
    pass