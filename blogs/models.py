from django.db import models
from login_and_sign.models import User
# Create your models here.



class Passage(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    #向外关联一个User类进来作为该user的外键，并以username表示