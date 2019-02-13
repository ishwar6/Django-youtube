from django import forms

from .models import Post


class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'blog_type', 'text', 'status'
        ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
