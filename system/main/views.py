from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm,RegisterForm,StockForm,TradeForm
from . import models
import hashlib
import tushare as ts
import mplfinance as mpf
import os
import sys
import datetime
import pandas as pd
import numpy as np
from .paint import paint
from .stockPredFinal import predictApi

# Create your views here.
token = '3b3eb46262e0ed413eb529f63de45817416cbef5932da6131f285507'
pro = ts.pro_api(token)

def login(request):
    if request.session.get('is_login',None):
        return redirect('/main/index')
 
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
                    return redirect('/main/index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！请先注册！"
                return redirect('/main/register')
        return render(request, 'main/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'main/login.html', locals())




def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/main/index")
    request.session.flush()
    return redirect("/main/index")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/main/index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            name = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'main/register.html', locals())
            else:
                same_name_user = models.user.objects.filter(username=name)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'main/register.html', locals())
                # 当一切都OK的情况下，创建新用户
 
                new_user = models.user.objects.create()
                new_user.username = name
                new_user.password = hash_code(password1)
                new_user.save()
                return redirect('/main/login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'main/register.html', locals())



def hash_code(s,salt='wyka'):
    h=hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    if request.method=="POST":
        stockClass=TradeForm(request.POST)
        try:
            stockModel=models.userStock.objects.get(username=request.session['user_name'],stockcode=stockClass.stockcode)
            stockModel.volume=stockModel.volume+stockClass.stockchange
            if stockModel.volume<0:
                message='交易失败！您所持有的股票不足！'
            elif stockModel.volume==0:
                stockModel.delete()
            else:
                stockModel.save()
            return render(request,'main/index.html',locals())
        except:
            models.userStock.create(
                username=request.session['user_name'],
                stockcode=stockClass.stockcode,
                volume=stockClass.stockchange
            )
            return render(request,'main/index.html',locals())
    else:
        stockcodes=models.userStock.objects.all(username=request.session['user_name'])
        stock_form=StockForm()
        return render(request,'main/index.html',locals())



def disp(request):
    if request.method == "POST":
        stock_form = StockForm(request.POST)
        message = "hello!"
        if stock_form.is_valid():
            code = stock_form.cleaned_data['stockcode']
            name = stock_form.cleaned_data['stockname']#获取股票信息
            today = datetime.date.today()#获取当日日期
            today = today.strftime('%Y%m%d')
            df = pro.daily(ts_code=code, trade_date='20210604')
            if df.empty:
                message="error!"
                return redirect('/main/main_page')#出错重定义到首页
            else:
                code= df.ts_code[0]
                open = df.open.values[0]
                high = df.high.values[0]
                low = df.low.values[0]
                pre_close = df.pre_close.values[0]
                change = df.change.values[0]
                paint(code,today)
                addr=f'./media/{code}.png'
            return render(request, 'main/disp.html', locals())
        stock_form = StockForm()
        return render(request, 'main/disp.html', )
    else:
        return render(request, 'main/disp.html', locals())

def main_page(request):
    forms = StockForm()
    return render(request, "main/main_page.html", locals())
