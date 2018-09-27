#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/10
# @Author  : suxianglun
# @Describe :
# @Version : 
from django.conf.urls import url,include
from blog import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.Archives.as_view(), name='archives'),
    url(r'category/(?P<pk>[0-9]+)$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)$', views.tag, name='tag'),

]
