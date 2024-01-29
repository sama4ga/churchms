from django.db import models
from django.urls import reverse
from organisation.models import OrganisationInfo
from church.extras import Status

class WorkingSociety(models.Model):
  name = models.CharField(max_length=200)
  organisation = models.ForeignKey(OrganisationInfo, on_delete=models.CASCADE, related_name='working_societies')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  class Meta:
    verbose_name_plural = 'Working Societies'
    # order_by = ['organisation']
  
  def __str__(self):
    return f'{self.name} society - {self.organisation}'
    
  def get_absolute_url(self):
    return reverse('working_society-view')
