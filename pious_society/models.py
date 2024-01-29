from django.db import models
from django.urls import reverse
from church.extras import Status

class PiousSociety(models.Model):
  name = models.CharField(max_length=200)
  slogan = models.CharField(max_length=100, blank=True)
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  class Meta:
    verbose_name_plural = 'Pious Societies'
  
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('pious_society-view')

