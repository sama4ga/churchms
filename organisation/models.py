from django.db import models
from django.urls import reverse
from station.models import Station
from church.extras import MeetingDay, MeetingDaySuffix, MeetingFreq, Status

class Organisation(models.Model):
  name = models.CharField(max_length=200)
  slogan = models.CharField(max_length=100)
  short_name = models.CharField(max_length=10)
  station = models.ManyToManyField(Station, related_name='organisations', through='OrganisationInfo')
  
  def __str__(self):
    return self.short_name
  
  def get_absolute_url(self):
    return reverse('organisation-view')
    
  class Meta:
    ordering = ['name']
    
  
class OrganisationInfo(models.Model):
  organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
  station = models.ForeignKey(Station, on_delete=models.CASCADE)
  meeting_days = models.CharField(choices=MeetingDay.choices, default=MeetingDay.SUNDAY, max_length=20)
  meeting_days_suff = models.CharField(choices=MeetingDaySuffix.choices, default=MeetingDaySuffix.NONE, max_length=20)
  meeting_frequency = models.CharField(choices=MeetingFreq.choices, default=MeetingFreq.MONTHLY, max_length=20)
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def meeting_info(self):
    return f'Every {self.meeting_days_suff} {self.meeting_days} - ({self.meeting_frequency})'
    
  def get_absolute_url(self):
    return reverse('organisation-view')
  
  def __str__(self):
    return f'{self.organisation.short_name} - {self.station.name}'
      