#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/15
# @Author  : suxianglun
# @Describe :
# @Version : 
from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag()
def get_archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_tags():
    return Tag.objects.all()
