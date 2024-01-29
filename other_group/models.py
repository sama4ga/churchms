from django.db import models
from django.urls import reverse
from church.extras import Status

class OtherGroup(models.Model):
  name = models.CharField(max_length=200)
  slogan = models.CharField(max_length=100, blank=True)
  short_name = models.CharField(max_length=10, blank=True)
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return self.short_name
    
  def get_absolute_url(self):
    return reverse('other_group-view')

