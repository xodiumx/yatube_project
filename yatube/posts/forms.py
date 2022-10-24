from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

        widgets = {
            'text': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите текст '
                }
            ),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите текст ',
                    'rows': 3,
                    'cols': 20,
                }
            ),
        }
