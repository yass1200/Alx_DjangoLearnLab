from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Enter comma-separated tags (e.g. python, django)'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_tags = ', '.join(t.name for t in self.instance.tags.all())
            self.fields['tags'].initial = current_tags

    def save(self, author=None, commit=True):
        instance = super().save(commit=False)
        if author is not None:
            instance.author = author
        if commit:
            instance.save()
            tags_str = self.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            instance.tags.set(tag_names)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
