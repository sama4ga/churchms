from django.db import models
from parishioner.models import Parishioner
from priest.models import Priest
from django.urls import reverse

class Matrimony(models.Model):
  bride = models.ForeignKey(Parishioner, on_delete=models.RESTRICT, related_name='brides')
  bride_parent = models.CharField(max_length=100)
  bride_village = models.CharField(max_length=100)
  groom = models.ForeignKey(Parishioner, on_delete=models.RESTRICT, related_name='grooms')
  groom_parent = models.CharField(max_length=100)
  groom_village = models.CharField(max_length=100)
  date = models.DateField()
  minister = models.ForeignKey(Priest, on_delete=models.RESTRICT)
  sponsor = models.CharField(max_length=100)
  sponsor_address = models.CharField(max_length=100)
  
  def __str__(self):
    return f'{self.bride.fullname} and {self.groom.fullname} marriage record'
    
  @property
  def regNo(self):
    return f'{self.pk}'
  
  def get_absolute_url(self):
    return reverse('matrimony-view')