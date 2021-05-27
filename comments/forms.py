from django.forms import ModelForm
from .models import Comments


class FormComments(ModelForm):
    def clean(self):
        data = self.cleaned_data
        # print(data)
        name_data = data.get('name_comment')
        email_data = data.get('email_comment')
        comment_data = data.get('comment')

        if len(name_data) < 8:
            self.add_error(
                'name_comment',
                'Nome precisa ter no mínimo oito caracteres.'
            )


    class Meta:
        model = Comments
        fields = ('name_comment', 'email_comment', 'comment')
