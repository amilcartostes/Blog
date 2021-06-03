from django.forms import ModelForm
from .models import Comments
from django.forms.widgets import TextInput, EmailInput, Textarea


class FormComments(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # To take : after the name

    def clean(self):
        data = self.cleaned_data
        name_data = data.get('name_comment')
        email_data = data.get('email_comment')
        comment_data = data.get('comment')

        if len(name_data) < 8:
            self.add_error(
                'name_comment',
                'Nome precisa ter mais que 8 caracteres.'
            )

    class Meta:
        model = Comments
        fields = ('name_comment', 'email_comment', 'comment')
        # labels = { No need because of the verbose 'name': 'Nome', 'description': 'Descrição', }
        widgets = {
            'name_comment': TextInput(attrs={
                'placeholder': 'Digite seu nome e sobrenome',
                'class': 'form-control',
            }),
            'email_comment': EmailInput(attrs={
                'placeholder': 'Digite seu e-mail',
                'class': 'form-control',
            }),
            'comment': Textarea(attrs={
                'placeholder': 'Digite seu cometário',
                'class': 'form-control',
                # 'rows': 5,
            }),
        }