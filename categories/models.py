from django.db import models


class Categories(models.Model):
    name_category = models.CharField(max_length=30, verbose_name='Categoria')

    def __str__(self):
        return self.name_category
