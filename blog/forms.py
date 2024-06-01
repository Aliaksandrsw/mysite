from django import forms

from blog.models import Comment, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags', 'body', 'status')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        if self.request and self.request.user.is_authenticated:
            self.instance.author = self.request.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = self.generate_slug(instance.title)
        if commit:
            instance.save()
        return instance

    def generate_slug(self, title):
        slug = title.replace(" ", "-").lower()
        # Проверяем, что slug уникален
        existing_slugs = Post.objects.filter(slug=slug).values_list('slug', flat=True)
        if slug in existing_slugs:
            # Добавляем уникальный суффикс, если slug уже существует
            suffix = 1
            while f"{slug}-{suffix}" in existing_slugs:
                suffix += 1
            slug = f"{slug}-{suffix}"
        return slug