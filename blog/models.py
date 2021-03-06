# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.conf import settings
class Category(models.Model):
    '''
    分类
    '''
    name = models.CharField(max_length=100)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField(max_length=100)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    # https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    # 文章标题
    title = models.CharField(max_length=100)
    # 文章内容
    body = models.TextField()
    # 创建时间
    create_time = models.DateField()
    # 最后一次修改时间
    modified_time = models.DateField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    # 分类 根据需求 一对多关系：一篇文章对应一个分类，一个分类有多个文章
    category = models.ForeignKey(Category)
    # 标签  根据需求 多对多关系： 一篇文章有多个标签，一个标签有多个文章
    tag = models.ManyToManyField(Tag, blank=True)
    # 作者
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # 阅读量 PositiveIntegerField 类型只允许其值大于等于0
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # 若没有摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54] + '......'
        super(Post, self).save(*args, **kwargs)

    def increate_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @python_2_unicode_compatible
    def __str__(self):
        return self.title

    class Meta:
        '''
        Post 类的内部定义一个 Meta 类，并指定排序属性：
        ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序，这里指定为按照文章发布时间排序，
        且负号表示逆序排列。列表中可以用多个项，比如 ordering = ['-created_time', 'title'] ，
        那么首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序。
        '''
        ordering = ['-create_time']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
