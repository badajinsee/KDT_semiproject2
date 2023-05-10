from django import forms
from .models import Post, PostImage, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
            'latitude',
            'longitude',
        )


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
        widgets = {'image': forms.FileInput(attrs={'multiple': True})}
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )