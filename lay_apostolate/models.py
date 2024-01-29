from django.db import models
from django.urls import reverse
from church.extras import Status

class LayApostolate(models.Model):
  name = models.CharField(max_length=200)
  slogan = models.CharField(max_length=100, blank=True)
  short_name = models.CharField(max_length=10, blank=True)
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('lay_apostolate-view')

