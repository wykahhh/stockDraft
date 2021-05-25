from django import forms
from captcha.fields import CaptchaField
from django.db.models.fields import CharField
from django.forms.widgets import PasswordInput

class UserForm(forms.Form):
    username=forms.CharField(label="用户名",max_length=128)
    password=forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    username=forms.CharField(label="用户名",max_length=128)
    password1=forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput)
    password2=forms.CharField(label="确认密码",max_length=256,widget=forms.PasswordInput)
    captcha=CaptchaField(label='验证码')