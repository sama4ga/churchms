from django.db import models
from church.extras import Position, Status
from parishioner.models import Parishioner
from station.models import Station
from django.urls import reverse

class Council(models.Model):
  name = models.CharField(max_length=100)
  station = models.ManyToManyField(Station, through='StationCouncil')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('council-view')

class StationCouncil(models.Model):
  council = models.ForeignKey(Council, on_delete=models.CASCADE, related_name='stations')
  station = models.ForeignKey(Station, on_delete=models.CASCADE, blank=True, null=True, related_name='councils')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.council}, {self.station}'
  
class CouncilHead(models.Model):
  council = models.ForeignKey(StationCouncil, on_delete=models.CASCADE, related_name='heads')
  position = models.CharField(choices=Position.choices, max_length=20)
  head = models.ForeignKey(Parishioner, on_delete=models.CASCADE, related_name='offices')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.position} {self.council}'
  
  def get_absolute_url(self):
    return reverse('council-head-view')
