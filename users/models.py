from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
  passport = models.ImageField(upload_to='users', default='user_default.jfif')
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile") #limit_choices_to={'groups__name': 'Testmanager'},
  
  def __str__(self):
    return self.user.username + ' profile'
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.passport.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.passport.path)