from django.db import models
from django.urls import reverse

class Event(models.Model):
  """Model definition for Event."""
  start = models.DateTimeField()
  end = models.DateTimeField()
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=400, blank=True)
  color = models.CharField(max_length=20)
  allDay = models.BooleanField(default=False)
  url = models.URLField(blank=True, null=True)
  event_type =  models.CharField(max_length=100, blank=True)

  class Meta:
    """Meta definition for Event."""

    verbose_name = 'Event'
    verbose_name_plural = 'Events'

  def __str__(self):
    """Unicode representation of Event."""
    return f'{self.title} event'


  def get_absolute_url(self):
    """Return absolute url for Event."""
    return (reverse('calendar-view-events'))

  

