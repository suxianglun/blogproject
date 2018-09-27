#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/9/27
# @Author  : suxianglun
# @Describe :
# @Version : 
from django.conf.urls import url, include
from users import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register')
]
