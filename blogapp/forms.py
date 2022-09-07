from django import forms
from mptt.forms import TreeNodeChoiceField

from blogapp.models import Comment, Category, Post


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
        fields = ('post', 'parent', 'content')
        widgets = {
            'content': forms.Textarea(attrs={"class": "ml-3 mb-3 form-control border-0"
                                                      "comment-add rounded-0",
                                             'rows': 1, 'placeholder': 'Add a public comment'})}

        def save(self, *args, **kwargs):
            Comment.objects.rebuild()
            return super(CommentForm, self).save(*args, **kwargs)


class SearchForm(forms.Form):
    q = forms.CharField()

    # categories = forms.ModelChoiceField(
    #     queryset=Category.objects.all().order_by('name')
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['categories'].required = False
        # self.fields['categories'].label = ''
        # self.fields['categories'].label = 'Category'
        # self.fields['categories'].widget.attrs.update({
        #     'class': 'my-3'})

        self.fields['q'].label = 'Search for'
        self.fields['q'].widget.attrs.update({
            'class': 'form-control menudd'})
        self.fields['q'].widget.attrs.update({
            'data-toggle': 'dropdown'})


choices = Category.objects.all().values_list('name', 'name')

choice_list = []
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'excerpt', 'content', 'status', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Type your title here'}),
            'excerpt': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Type your tag here'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'value': '', 'type': 'hidden',
                                             'id': 'usernameId'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
        }
