#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/20
# @Author  : suxianglun
# @Describe :
# @Version :
from django import forms
from comments.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 表单所显示的的字段
        fields = ['name', 'email', 'url', 'text']
