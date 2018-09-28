#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/9/28
# @Author  : suxianglun
# @Describe : 邮箱后台认证
# @Version : 
from users.models import User


class EmailBackend(object):
    def authenticate(self, **kwargs):
        emial = kwargs.get('email', kwargs.get('username'))
        try:
            user = User.objects.filter(email=emial)[0]
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(kwargs.get('password')):
                return user

    def get_user(self, user_id):
        '''
        该方法是必须的
        :return:
        '''
        try:
            return User.objects.filter(pk=user_id)
        except User.DoesNotExist:
            return None
