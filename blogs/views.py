from django.shortcuts import render
from django.views.generic import DetailView
# Create your views here.

def home(request):
    return render(request, 'home.html')
