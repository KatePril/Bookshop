from django.db import models
from shop.models import Book
from blog.models import Article
from django.contrib.auth import get_user_model

# Create your models here.
class CommentBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='commentsBook')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='commentsBook')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.book.name} - {self.text}'
    
    class Meta:
        ordering = ['-created_at']

class CommentArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentsArticle')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='commentsArticle')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.article.title} - {self.text}'
    
    class Meta:
        ordering = ['-created_at']