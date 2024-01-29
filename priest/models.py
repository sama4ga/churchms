from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Priest(models.Model):
  
  class PriestType(models.TextChoices):
    PARISH_PRIEST = "PP", _("Parish Priest")
    ASST_PARISH_PRIEST = "APP", _("Asst. Parish Priest")
    PRIEST_IN_RESIDENCE = "PIR", _("Priest in Residence")
    
  name = models.CharField(max_length=100)
  email = models.EmailField(blank=True)
  phone_number = models.CharField(max_length=14)
  type = models.CharField(choices=PriestType.choices, default=PriestType.PARISH_PRIEST, max_length=3)
  passport = models.ImageField(upload_to='priests', default='priest_default.jfif')
  date_of_birth = models.DateField()
  date_ordained = models.DateField()
  date_resumed = models.DateField()
  date_transfered = models.DateField(blank=True, null=True)
  
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('priest-view')
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    print(self.passport)
    img = Image.open(self.passport.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.passport.path)

