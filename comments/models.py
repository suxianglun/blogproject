from django.db import models
from django.utils.six import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()

    create_time = models.DateField(auto_now_add=True)
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]
