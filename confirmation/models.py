from django.db import models
from parishioner.models import Parishioner
from priest.models import Priest
from django.urls import reverse

class Confirmation(models.Model):
  candidate = models.ForeignKey(Parishioner, on_delete=models.RESTRICT)
  date = models.DateField()
  minister = models.CharField(max_length=100)
  sponsor = models.CharField(max_length=100)
  
  def __str__(self):
    return f'{self.candidate.fullname} confirmation record'
    
  @property
  def regNo(self):
    return f'{self.pk}'
  
  def get_absolute_url(self):
    return reverse('confirmation-view')