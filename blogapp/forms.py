from django import forms
from mptt.forms import TreeNodeChoiceField

from blogapp.models import Comment, Category


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


class SearchForm(forms.Form):
    q = forms.CharField()
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].required = False
        self.fields['categories'].label = ''
        self.fields['categories'].label = 'Category'
        self.fields['categories'].widget.attrs.update({
            'class': 'my-3'})

        self.fields['q'].label = 'Search for'
        self.fields['q'].widget.attrs.update({
            'class': 'form-control menudd'})
        self.fields['q'].widget.attrs.update({
            'data-toggle': 'dropdown'})
