from django.shortcuts import render,redirect
from django.db import models
from .forms import RegisterForm, UserForm
import hashlib
# Create your views here.

def index(request):
    pass
    return render(request,'index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')

    if request == 'POST':
        login_form=UserForm(request.POST)
        message="请检查填写的内容！"
        if login.form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            try:
                user=models.User.objects.get(name=username)
                if user.password==password:
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name']=user.name #设置用户为登录状态
                    return redirect('/index/')
                else:
                    message="密码不正确！"
            except:
                message="用户不存在！"
        return render(request,'login.html',locals())

    login_form=UserForm()
    return render(request,'login.html',locals())



def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/index")
    request.session.flush()
    return redirect("/index/")



def register(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method=="POST":
        register_form=RegisterForm(request.POST)
        message="请检查填写的内容！"
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            if password1 != password2: #判断两次输入的密码是否相同
                message = "两次输入的密码不同！"
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.Users.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新输入用户名！'
                    return render(request,'login/register.html',locals())

            #验证均通过后，创建新用户
            new_user=models.Users.objects.create()
            new_user.name=username
            new_user.password=password1
            new_user.save()
            return redirect('/login/') #自动跳转到登录页面
    register_form=RegisterForm()
    return render(request,'login/register.html',locals())



def hash_code(s,salt='mysite'):
    h=hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()