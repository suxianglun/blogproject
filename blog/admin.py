from django.contrib import admin
from blog.models import Post, Category, Tag


# Register your models here.
# 通过注册PostAdmin 继承admin.ModelAdmin 自定义Post
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
