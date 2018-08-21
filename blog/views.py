import markdown
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm


# Create your views here.

def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    '''
    详情页
    :param request:
    :param pk:
    :return:
    '''
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    # 在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
    }

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    '''
    归档
    :param request:
    :param year:
    :param month:
    :return:
    '''
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    '''
    分类：先根据分类id 从分类表中查分类
    :param request:
    :param pk:
    :return:
    '''
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    '''
    标签
    :param request:
    :param pk:
    :return:
    '''
    tag_obj = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tag=tag_obj).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
