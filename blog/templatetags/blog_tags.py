#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/15
# @Author  : suxianglun
# @Describe :
# @Version : 
from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag()
def get_archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag()
def get_categories():
    # Count()计算各个分类下文章数
    # post 告诉Count（）是Post模型
    # gt 就是 greate than，表示大于，不是大于等于。大于等于是 gte
    return Category.objects.annotate(nums_posts=Count('post')).filter(nums_posts__gt=0)


@register.simple_tag()
def get_tags():
    return Tag.objects.annotate(nums_posts= Count('post')).filter(nums_posts__gt=0)
