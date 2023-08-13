from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from config.settings import PAGE_NAMES
from .models import Article, Tag
from main.mixins import ListViewBreadCrumbMixin, DetailViewBreadcrumbsMixin

from comments.models import CommentArticle
from comments.forms import CommentArticleForm

class BlogIndexView(ListViewBreadCrumbMixin):
    template_name = 'blog/index.html'
    model = Article
    
    def get_queryset(self):
        return Article.objects.filter(is_popular=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['articles'] = Article.objects.filter(is_popular=True)
        return context
    
    def get_breadcrumbs(self):
        self.breadcrumbs = {
            'current' : PAGE_NAMES['blog'],
        }
        return self.breadcrumbs

class AllArticlesView(ListViewBreadCrumbMixin):
    template_name ='blog/article_list.html'
    tags = Tag.objects.all()
    
    def get_queryset(self):
        return Article.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.tags
        context['articles'] = Article.objects.all()
        return context
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('blog'): PAGE_NAMES['blog']}
        breadcrumbs.update({'current': 'All articles'})
        return breadcrumbs

class AllTagsView(ListViewBreadCrumbMixin):
    template_name ='blog/all_tags.html'
    
    def get_queryset(self):
        return Tag.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context
    

class ArticleByTag(ListViewBreadCrumbMixin):
    template_name = 'blog/article_list.html'
    tag = None
    tags = Tag.objects.all()
    model = Article
    
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.tag = Tag.objects.filter(slug=self.kwargs['slug'])
    #     return queryset
    
    def get_queryset(self):
        self.tag = Tag.objects.filter(slug=self.kwargs['slug'])
        articles = Article.objects.filter(tags__slug=self.kwargs['slug'])
        return articles
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.tags
        context['articles'] = Article.objects.filter(tags__slug=self.kwargs['slug'])
        return context
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('blog'): PAGE_NAMES['blog']}
        # breadcrumbs.update({'current': self.tag.name})
        return breadcrumbs

class ArticleDetailView(DetailViewBreadcrumbsMixin):
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('blog'): PAGE_NAMES['blog']}
        breadcrumbs.update({'current': self.article.title})
        return super().get_breadcrumbs()
    
    def get(self, request, slug):
        form = CommentArticleForm()
        article = Article.objects.filter(slug=slug).first()
        comments = CommentArticle.objects.filter(article=article)
        return render(request, 'blog/article_detail.html', {'form': form, 'article': article, 'comments': comments})
    
    def post(self, request, slug):
        form = CommentArticleForm(request.POST, request.FILES)
        article = Article.objects.filter(slug=slug).first()
        comments = CommentArticle.objects.filter(article=article)
        if form.is_valid():
            comment = form.save(user=request.user, article=article)
            return redirect('article', slug=slug)
        return render(request, 'blog/article_detail.html', {'form': form, 'article': article, 'comments': comments})
    
def user_article_list(request, pk):
        articles = Article.objects.filter(author=pk)
        return render(request, 'blog/custom_list.html', {'articles': articles})

def delete_article(request, pk, slug):
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    return redirect('user_articles', pk=pk)

def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect('all_tags')