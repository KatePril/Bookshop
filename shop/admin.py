from django.contrib import admin
from .models import Category, Book, Image


class BookCategoryInline(admin.TabularInline):
    model = Book.category.through
    extra = 1
    
class ImageInline(admin.TabularInline):
    model = Image
    fields = ('book', 'image_tag', 'image', 'is_main')
    readonly_fields = ('image_tag',)
    extra = 1


admin.site.register(Image)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'image_tag_thumbnail')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_tag_thumbnail',)
    fields = ('name', 'slug', 'parent', 'description','image_tag_thumbnail', 'image',
                'meta_title', 'meta_description', 'meta_keywords')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description', 'quantity', 'price', 'is_best_saled', 'meta_title', 'meta_description', 'meta_keywords', 'owner')
    list_display = ('id', 'name', 'quantity', 'price', 'is_best_saled')
    list_display_links = ('id', 'name')
    inlines = (BookCategoryInline, ImageInline)