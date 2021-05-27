from django.contrib import admin
from .models import Comments


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_comment', 'email_comment', 'post_comment', 'data_comment', 'published_comment',)
    list_editable = ('published_comment',)
    list_display_links = ('id', 'name_comment', 'email_comment',)


admin.site.register(Comments, CommentAdmin)
