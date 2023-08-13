from django.contrib import admin
from .models import Tag, Article
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'tags', 'related_book', 'preview', 'text', 'status', 'image', 'is_popular', 'author')
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')