from django import forms

from .models import Post


class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
<<<<<<< HEAD
        fields = [
            'title', 'blog_type', 'text', 'status'
        ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
=======
        exclude = ('id', 'slug')
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

>>>>>>> 542bfc8a32b0feee925334932b25bfc4701f3498
