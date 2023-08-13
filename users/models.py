from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.

class UserProfile(AbstractUser):
    phone = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = ProcessedImageField(
        upload_to='users',
        processors=[],
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True
        )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70}
    )
    github = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    def make_admin(self):
        self.is_admin = True
        self.save()