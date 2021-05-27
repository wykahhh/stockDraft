from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    pass
    return render(request,'user/index.html')

def login(request):
    pass
    return render(request,'user/login.html')

def register(request):
    pass
    return render(request,"user/register.html")

def logout(request):
    pass
    return render(request,"/index/")