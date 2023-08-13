from django import forms
from .models import CommentBook, CommentArticle

class CommentBookForm(forms.ModelForm):
    class Meta:
        model = CommentBook
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
    
    def save(self, user, book, commit=True):
        comment = super().save(commit=False)
        comment.user = user
        comment.book = book
        if commit:
            comment.save()
        return comment
class CommentArticleForm(forms.ModelForm):
    class Meta:
        model = CommentArticle
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
    
    def save(self, user, article, commit=True):
        comment = super().save(commit=False)
        comment.user = user
        comment.article = article
        if commit:
            comment.save()
        return comment