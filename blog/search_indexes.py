#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @Date    : 2018/8/27
# @Author  : suxianglun
# @Describe :
# @Version : 
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    '''
    在 blog 应用下建立一个 search_indexes.py 文件这是 django haystack 的规定。要相对某个 app 下的数据进行全文检索，
    就要在该 app 下创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post），
    并且继承 SearchIndex 和 Indexable。
    '''
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
