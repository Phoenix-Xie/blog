from django.db import models
from . import setting
# Create your models here.

class User(models.Model):
    #id = models.AutoField(primary_key=True)
    #该字段会被自动添加进去
    #字段自述名会将变量名下划线换为空格后作为自述名
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    username = models.CharField(max_length=setting.the_largest_length_of_username, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=setting.the_largest_length_of_password_for_database, verbose_name='密码')
    email = models.CharField(max_length=setting.the_largest_length_of_email, verbose_name='邮箱')

    def __str__(self):
        return self.username

