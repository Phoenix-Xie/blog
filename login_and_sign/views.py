from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect
from .models import User
from blogs import  views
from django.urls import reverse
# Create your views here.


def login(request):
    return render(request, 'login.html')


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = get_object_or_404(User, username=username)
        if user.password == password:
            HttpResponseRedirect(views.home)

def sign(request):
    return render(request, "sign.html")
