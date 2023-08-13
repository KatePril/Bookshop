import uuid

from django.db import models
from django.utils.text import slugify

from django.contrib.admin import display
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from main.mixins import MetaTagMixin
from mptt.models import MPTTModel, TreeForeignKey

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from ckeditor.fields import RichTextField

MEDIA_ROOT = settings.MEDIA_ROOT

# Create your models here.
class Category(MPTTModel, MetaTagMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        to = 'self',
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True
    )
    image = ProcessedImageField(
        upload_to='category/',
        processors=[ResizeToFill(600, 400)],
        format='JPEG',
        options={'quality': 70},
        blank=True,
        null=True,
    )
    
    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return " -> ".join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})
    
    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="70">')
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}">')
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}_{uuid.uuid4()}')
        super().save(*args, **kwargs)

class Book(MetaTagMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_best_saled = models.BooleanField(default=False)
    category = models.ManyToManyField(
        to=Category,
        through = 'BookCategory',
        related_name='books'
    )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def images(self):
        return Image.objects.filter()
    
    def main_image(self):
        image = Image.objects.filter(book=self.id, is_main=True).first()
        if image:
            return image      
        image = Image.objects.filter(book=self.id).first()
        if image:
            return image
        return Image.objects.filter().first()
    
    def get_absolute_url(self):
        return reverse('book', kwargs={'slug': self.slug})
    
    def main_category(self):
        category = self.category.filter(bookcategory__is_main=True).first() # вибираємо категорію яка має is_main=True
        if category:
            return category
        return self.category.first()
     
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}_{uuid.uuid4()}')
        super().save(*args, **kwargs)

class BookCategory(models.Model):
    book = models.ForeignKey(Book, verbose_name='Товар', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основна', default=False)
    
    def __str__(self):
        return f'{self.book.name} - {self.category.name}'
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_main:
            BookCategory.objects.filter(book=self.book, is_main=True).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)
        
    class Meta:
        verbose_name = 'Категорія товару'
        verbose_name_plural = 'Категорії товарів'

class Image(models.Model):
    image = ProcessedImageField(
        upload_to='book/',
        processors=[],
        format='JPEG',
        options={'quality': 100},
        null=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 70}
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='images'
    )
    is_main = models.BooleanField(default=False)
    
    @display(description='Image')
    def image_tag_thumbnail(self):
        if self.image:
            if not self.image_thumbnail:
                Image.objects.get(id=self.id)
            return mark_safe(f'<img src="{self.image_thumbnail.url}" height="70">')
        
    @display(description='Image')
    def image_tag(self):
        if self.image:
            if not self.image_thumbnail:
                Image.objects.get(id=self.id)
            return mark_safe(f'<img src="{self.image_thumbnail.url}">')
        
    def set_main(self):
        images = Image.objects.filter(book=self.book)
        print(images)
        for image in images:
            image.is_main = False
            image.save()
        self.is_main = True
        self.save()