from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comments(models.Model):
    name_comment = models.CharField(max_length=150, verbose_name='Nome')
    email_comment = models.EmailField(verbose_name='E-mail')
    comment = models.TextField(verbose_name='Comentário')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    user_comment = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Usuário')
    data_comment = models.DateTimeField(default=timezone.now, verbose_name='Data')
    published_comment = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.name_comment
