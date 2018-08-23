import markdown
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView


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


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class PostDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(self, request, *args, **kwargs)
        self.object.increat_vies()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
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
