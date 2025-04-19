from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default_pic.jpg', upload_to='profile_pics')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def image_url(self):
        try:
            # Check if image exists and has been explicitly set (not default)
            if self.image and hasattr(self.image, 'url') and self.image.name != 'profile_pics/default_pic.jpg':
                return self.image.url
            else:
                # Return the default image path from within the project
                return f"{settings.MEDIA_URL}profile_pics/default_pic.jpg"
        except Exception:
            # In case of any error, return the default image
            return f"{settings.MEDIA_URL}profile_pics/default_pic.jpg"
    # Create your models here.
