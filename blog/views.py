import markdown
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
class IndexView(ListView):
    # 将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。首先通过  从数据库中获取文章（Post）列表数据Post.objects.all()，并将其保存到 post_list 变量中
    # 类视图中这个过程 ListView 帮我们做了
    model = Post
    # template_name。指定这个视图渲染的模板。
    template_name = 'blog/index.html'
    # context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板
    context_object_name = 'post_list'

    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 分页器
        paginator = context.get('paginator')
        # 页面对象
        page = context.get('page_obj')
        # 布尔值 是否分页
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        # 分页的总页数
        total_pages = paginator.num_pages
        # 当前页页数
        page_num = page.number
        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range
        # 当前页面左边页码列表
        left = []
        # 当前页面右边页码列表
        right = []
        # 是否显示第一页
        first = False
        # 是否显示最后一行
        last = False
        # 是否显示当前页左边的省略号
        left_has_more = False
        # 是否显示当前页面右边的省略号
        right_has_more = False

        if page_num == 1:  # 当前页面是第一页
            # 左边的页码列表为空，只计算右边页码列表  [1, 2, 3, 4, 5, 6, 7, 8, 9 ]  [1, 2, 3, ]
            right = page_range[page_num:(page_num + 4) if page_num + 4 < total_pages else total_pages]
            # 由于当前页面已经是第一页了，所有不需要再显示第一页了，否则会重复
            first = False
            # 不显示左边的省略号, 当前页面右边页码列表最后页码小于倒数第二页，显示右边省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_num == total_pages:  # 当前页面是最后一页  [1, 2, 3, 4, 5, 6, 7, 8, 9 ] [ 1, 2, 3 ]
            left = page_range[(page_num - 4) if page_num - 4 > 0 else 0:page_num - 1]
            # 显示第一页，由于当前页面已经是最后 一页了，不再显示最后一页
            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True

        else:  # [1, 2, 3, 4, 5, 6, 7, 8, 9 ]
            left = page_range[(page_num - 4) if page_num - 4 > 0 else 0:page_num - 1]
            right = page_range[page_num:page_num + 3]
            if left[0] > 1:
                first = True
            if left[0] > 2:
                left_has_more = True
            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(self, request, *args, **kwargs)
        self.object.increate_views()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        # convert 方法将 post.body 中的 Markdown 文本渲染成 HTML 文本
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data目的不仅要将post传给模板（DetailView已经帮我们做了），还要将评论及表单传给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context



def detail(request, pk):
    '''
    详情页
    :param request:
    :param pk:
    :return:
    '''
    post = get_object_or_404(Post, pk=pk)
    # 增加阅读量并保存到数据库
    post.increate_views()
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


class Archives(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(Archives, self).get_queryset().filter(created_time__year=year, created_time__month=month)


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


class CategoryView(IndexView):
    '''
    由于CategoryView model template_name context_object_name需要指定和IndexView是一样的，直接继承IndexView即可
    '''

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset(category=cate)


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
