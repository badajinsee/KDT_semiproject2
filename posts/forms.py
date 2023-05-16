from django import forms
from django.forms import Textarea
from .models import Post, PostImage, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
            'latitude',
            'longitude',
            'location',
        )
        widgets = {
            'content' : Textarea(attrs={
                'style': "width:400px; height:272px; margin-top: 10px; margin-bottom: 10px; border:none; border-bottom:1px solid lightgray;" ,'placeholder':"내용을 입력해주세요."
            }),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
        widgets = {'image': forms.FileInput(attrs={'multiple': True, 'name': 'image'})}
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )