from django import forms
from mptt.forms import TreeNodeChoiceField

from blogapp.models import Comment


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].label = ''
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={"class": "col-sm-12"}),
            'email': forms.TextInput(attrs={"class": "col-sm-12"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
        }
