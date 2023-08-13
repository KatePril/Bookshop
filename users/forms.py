from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from shop.models import Book, Image, Category
from blog.models import Article, Tag

class SingupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'image', 'github', 'twitter', 'instagram', 'facebook')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'github':forms.TextInput(attrs={'class':'form-control'}),
            'twitter':forms.TextInput(attrs={'class':'form-control'}),
            'instagram':forms.TextInput(attrs={'class':'form-control'}),
            'facebook':forms.TextInput(attrs={'class':'form-control'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'class':'form-control'})


class BookForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Book
        fields = ('name','description', 'quantity', 'price', 'is_best_saled', 'category')
        widgets = {
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, user):
        book = super().save(commit=False)
        book.owner = user
        book.save()
        print(book.category)
        
            
        print(book.id)
        if self.cleaned_data['image']:
            Image.objects.create(book=book, image=self.cleaned_data['image'], is_main=True)
        return book

class ArticleForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Article
        fields = ('title','related_book', 'tags', 'preview', 'text', 'status', 'is_popular')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'related_book': forms.Select(attrs={'class': 'form-control'}),
            'preview': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def save(self, user):
        article = super().save(commit=False)
        article.author = user
        
        if self.cleaned_data['image']:
            article.image = self.cleaned_data['image']
        
        
        return article

class CategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Category
        fields = ('name', 'description', 'parent')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def save(self):
        category = super().save(commit=False)
        
        if self.cleaned_data['image']:
            category.image = self.cleaned_data['image']
        
        return category

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }