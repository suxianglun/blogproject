from django.shortcuts import render, redirect
from users.forms import RegisterForm


# Create your views here.

def register(request):
    # 先从 post 请求中获取 next 参数值,如果没有再从get请求中获取next
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_url =request.POST.get('next', request.GET.get('next'))
    if request.method == "POST":
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        form = RegisterForm(request.POST)
        # 校验form表单的合法性
        if form.is_valid():
            # 保存到数据库
            form.save()
            # 重定向到登录页
            return redirect('../login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form, 'next':redirect_url})
