from django.contrib import admin
from .models import Categories


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category',)
    list_display_links = ('id', 'name_category',)


admin.site.register(Categories, CategoryAdmin)
