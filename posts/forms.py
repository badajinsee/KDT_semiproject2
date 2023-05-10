from django import forms
from .models import Post, PostImage

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