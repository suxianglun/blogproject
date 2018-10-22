import markdown
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q


# Create your views here.
class IndexView(ListView):
    '''
    属性
    context_object_name————在模板中的变量名。{{name}}
    template_name————-模板一般是一个html文件名
    paginate_by————如果做分页这个参数说明每页有几个item项
    model——————对应的模型（Model）
    http_method_names———-请求类型 可以是get或者post

    方法
    get_queryset——–或者需要展示的数据并且返回（必须要有返回）
    get_context_data——–传递额外的数据到模板（html）。
    '''
    # 将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。首先通过  从数据库中获取文章（Post）列表数据Post.objects.all()，并将其保存到 post_list 变量中
    # 类视图中这个过程 ListView 帮我们做了
    model = Post
    # template_name。指定这个视图渲染的模板。
    template_name = 'blog/index.html'
    # context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板
    context_object_name = 'post_list'
    # 每页有几个item项
    paginate_by = 4
    # 排序
    ordering = '-id'


    def get_context_data(self, **kwargs):
        """ 在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
                例如 render(request, 'blog/index.html', context={'post_list': post_list})，
                这里传递了一个 {'post_list': post_list} 字典给模板。
                在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
                所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """
        context = super().get_context_data(**kwargs)
        # 分页器
        paginator = context.get('paginator')
        # 页面对象
        page = context.get('page_obj')
        # 布尔值 是否分页
        is_paginated = context.get('is_paginated')
        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典
        context.update(pagination_data)
        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
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
        # 是否显示最后一页
        last = False
        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        if page_num == 1:  # 当前页面是第一页
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_num:page_num + 2]
            first = False
            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True
        elif page_num == total_pages:  # 当前页面是最后一页  [1, 2, 3, 4, 5, 6, 7, 8, 9 ] [ 1, 2, 3 ]
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True

        else:  # [1, 2, 3, 4, 5, 6, 7, 8, 9 ]
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_num - 3) if (page_num - 3) > 0 else 0:page_num - 1]
            right = page_range[page_num:page_num + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
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

    def post(self, request):
        return


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
    '''
    归档
    '''

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(Archives, self).get_queryset().filter(create_time__year=year, create_time__month=month)


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
    分类
    由于CategoryView model    template_name    context_object_name需要指定和IndexView是一样的，直接继承IndexView即可
    '''

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 该方法默认获取指定模型的全部列表数据。为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为。
        return super(CategoryView, self).get_queryset().filter(category=cate).order_by('-create_time')


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


class TagView(IndexView):
    '''
    标签
    '''

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        # post_list = Post.objects.filter(tag=tag_obj).order_by('-create_time')
        return super(TagView, self).get_queryset().filter(tag=tag).order_by('-create_time')


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


def search(request):
    q = request.GET.get('q')
    err_msg = ''
    if not q:
        err_msg = '无法搜索到相关内容'
        return render(request, 'blog/index.html', {'err_msg': err_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'err_msg': err_msg, 'post_list': post_list})
