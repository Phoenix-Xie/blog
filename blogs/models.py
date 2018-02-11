from django.db import models
from login_and_sign.models import User
# Create your models here.



class Passage(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    title = models.CharField(max_length=30)
    pub_time = models.DateTimeField()
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50)
    type3 = models.CharField(max_length=50)
    #向外关联一个User类进来作为该user的外键，并以username表示