from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q, Count, Case, When
from django.contrib import messages
from django.db import connection
from .models import Post
from comments.forms import FormComments
from comments.models import Comments


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts_objects'

    # Override the query set to change the order in which posts are displayed
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category_post')
        qs = qs.order_by('-id').filter(published_post=True)
        qs = qs.annotate(
            number_comments=Count(
                Case(
                    When(comments__published_comment=True, then=1)
                )
            )
        )
        return qs

    # To monitor the quantities of database queries
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connection'] = connection
        return context


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'

    # Filter the query set to search term
    def get_queryset(self):
        qs = super().get_queryset()
        # print(self.request.GET.get('term'))
        term = self.request.GET.get('term')

        if not term:
            return qs

        qs = qs.filter(
            Q(title_post__icontains=term) |
            Q(author_post__first_name__iexact=term) |
            Q(data_post__icontains=term) |
            Q(content_post__icontains=term) |
            Q(excerpt_post__icontains=term) |
            Q(category_post__name_category__iexact=term)
        )
        return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    # Filter the query set to select the category
    def get_queryset(self):
        qs = super().get_queryset()
        # print(self.kwargs)
        category = self.kwargs.get('category', None)
        if not category:
            return qs
        qs = qs.filter(category_post__name_category__iexact=category)
        return qs


class PostDetails(UpdateView):
    template_name = 'posts/post_detail.html'
    model = Post
    form_class = FormComments
    context_object_name = 'post_objects'

    # Override the get_context_data method
    def get_context_data(self, **kwargs):
        # Using what you already have in get_context_data
        context = super().get_context_data(**kwargs)
        # Getting which post we're working on
        post = self.get_object()
        # Selecting information from the database and injecting it in context
        comments = Comments.objects.filter(published_comment=True,
                                           post_comment=post.id)
        context['comments'] = comments
        return context

    def form_valid(self, form):
        post = self.get_object()
        comment = Comments(**form.cleaned_data)
        # Complete the comment table fields provided in which post the comment was made
        comment.post_comment = post
        # Checks if the user is logged in to enter it as user_comment
        if self.request.user.is_authenticated:
            comment.user_comment = self.request.user
        # Save the comment, send a message to the user and redirect to the detail page of the post
        comment.save()
        messages.success(self.request, 'Comentario gravado com sucesso!')
        return redirect('post_details', pk=post.id)
