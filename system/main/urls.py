from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('index/',views.index),
    path('disp/',views.disp),
    path('main_page/',views.main_page)
]