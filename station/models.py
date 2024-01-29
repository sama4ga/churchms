from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from church.extras import Status
from PIL import Image

class Station(models.Model):
  name = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  date_created = models.DateField(default=datetime.today)
  picture = models.ImageField(upload_to='station_pictures', default="church_default.jfif")
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.name} station'
    
  def get_absolute_url(self):
    return reverse('station-view')
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.picture.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.picture.path)

