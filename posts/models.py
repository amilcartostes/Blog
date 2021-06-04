from django.db import models
from categories.models import Categories
from django.contrib.auth.models import User
from django.utils import timezone
# Imported modules for image resizing
from PIL import Image
from django.conf import settings
import os


class Post(models.Model):
    title_post = models.CharField(max_length=255, verbose_name='Título')
    author_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data')
    content_post = models.TextField(verbose_name='Conteúdo')
    excerpt_post = models.TextField(verbose_name='Excerto')
    category_post = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      verbose_name='Categoria')
    image_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True, verbose_name='Imagem')
    published_post = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.title_post

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Resize the image
        if self.image_post:
            self.resize_image(self.image_post.name, 800)

    @staticmethod
    def resize_image(image_name, new_width):
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        # print(f'{image_path}')
        # Open the image with Pillow
        img = Image.open(image_path)
        # Getting the original width and height of the image
        width, height = img.size
        # Does not resize images with the same width or smaller width
        if width <= new_width:
            img.close()
            return
        # Determining the new height of the image
        new_height = round((new_width * height) / width)
        # Resizing the image
        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        # Salvando a imagem sobre a imagem original
        new_img.save(
            image_path,
            optimize=True,
            quality=60,
        )
        new_img.close()


