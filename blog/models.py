import uuid

from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

from shop.models import Book
# Create your models here.
class Article(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'
    
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft'),
    )
    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles',  default=1)
    related_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    tags = models.ManyToManyField('Tag', related_name='articles')
    title = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name='URL', unique=True)
    preview = models.TextField()
    text = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}_{uuid.uuid4()}')
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(verbose_name='URL', default='', unique=True)
    
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}_{uuid.uuid4()}')
        super().save(*args, **kwargs)