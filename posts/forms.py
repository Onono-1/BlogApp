from django import forms

from .models import Comment, Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','thumbnail','banner','content']

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control'}),
			'thumbnail':forms.FileInput(attrs={'class':'form-control'}),
			'banner':forms.FileInput(attrs={'class':'form-control'}),
			'content':forms.Textarea(attrs={'class':'form-control'}),
		}

	

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

