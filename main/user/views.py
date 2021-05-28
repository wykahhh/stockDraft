from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm,RegisterForm
from . import models
import hashlib

# Create your views here.

def login(request):
    if request.session.get('is_login',None):
        return redirect('user/index.html')
 
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.user.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('user:index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'user/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'user/login.html', locals())



def logout(request):
    if not request.session.get('is_login', None):
        return redirect("user/index.html")
    request.session.flush()
    return redirect("user/index.html")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("user:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'user/register.html', locals())
            else:
                same_name_user = models.user.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'user/register.html', locals())
                # 当一切都OK的情况下，创建新用户
 
                new_user = models.user.objects.create()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.save()
                return redirect('user/login.html')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'user/register.html', locals())



def hash_code(s,salt='wyka'):
    h=hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    pass
    return render(request,'user/index.html')