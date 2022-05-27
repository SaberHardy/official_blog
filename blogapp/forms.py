from django import forms

from blogapp.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={"class": "col-sm-12"}),
            'email': forms.TextInput(attrs={"class": "col-sm-12"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
        }
