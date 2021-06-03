from django import template

# Create variable that will be used to decorate the templates
register = template.Library()


# Plural filter for the word 'Comment(s)' to be applied to template ./blog/templates/posts/index.html
# Registering the filter
@register.filter(name='plural_comments')
def plural_comments(num_comments):
    try:
        num_comments = int(num_comments)
        if num_comments == 0:
            return f'Sem comentários'
        elif num_comments == 1:
            return f'{num_comments} Comentário'
        else:
            return f'{num_comments} Comentários'
    except:
        return f'{num_comments} Comentário(s)'
