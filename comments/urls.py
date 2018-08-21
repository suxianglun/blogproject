#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/20
# @Author  : suxianglun
# @Describe :
# @Version : 
from django.conf.urls import url
from comments import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]
