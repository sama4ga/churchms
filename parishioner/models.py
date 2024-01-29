from django.db import models
from django.urls import reverse
from station.models import Station
from organisation.models import OrganisationInfo
from society.models import WorkingSociety
from other_group.models import OtherGroup
from pious_society.models import PiousSociety
from lay_apostolate.models import LayApostolate
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from church.extras import Status, MaritalStatus
from PIL import Image

class Parishioner(models.Model):
  title = models.CharField(max_length=100)
  surname = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  middle_name = models.CharField(max_length=100, blank=True)
  reg_no = models.CharField(max_length=20, blank=True)
  phone_number = models.CharField(max_length=14, blank=True)
  occupation = models.CharField(max_length=100, blank=True)
  residential_address = models.CharField(max_length=200)
  home_address = models.CharField(max_length=200, blank=True)
  office_address = models.CharField(max_length=200, blank=True)
  diocese_of_origin = models.CharField(max_length=100)
  parish_of_origin = models.CharField(max_length=100)
  state_of_origin = models.CharField(max_length=100)
  lga_of_origin = models.CharField(max_length=100)
  email = models.EmailField(blank=True)
  passport = models.ImageField(upload_to='passports', default='user_default.jfif')
  marital_status = models.CharField(choices=MaritalStatus.choices, default=MaritalStatus.SINGLE, max_length=10)
  gender = models.CharField(choices=[('Male','Male'),('Female','Female')], max_length=10)
  date_of_birth = models.DateField()
  spouse_name = models.CharField(max_length=100, blank=True)
  station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="members")
  station_status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  organisation = models.ForeignKey(OrganisationInfo, on_delete=models.SET_NULL, null=True, related_name='members')
  organisation_status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  working_society = models.ForeignKey(WorkingSociety, on_delete=models.SET_NULL, null=True, related_name='members')
  working_society_status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  other_group = models.ManyToManyField(OtherGroup, blank=True, related_name='members', through='OtherGroupInfo')
  pious_society = models.ManyToManyField(PiousSociety, blank=True, related_name='members', through='PiousSocietyInfo')
  lay_apostolate = models.ManyToManyField(LayApostolate, blank=True, related_name='members', through='LayApostolateInfo')
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parishioners_created')
  created_on = models.DateTimeField(auto_now_add=True)
  modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parishioners_modified')
  modified_on = models.DateTimeField(auto_now=True)
  deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='parishioners_deleted')
  deleted_on = models.DateTimeField(null=True, editable=False, blank=True)
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  baptised = models.BooleanField()
  communicant = models.BooleanField()
  confirmed = models.BooleanField()
  wedded = models.BooleanField()
  charisma = models.TextField()
  
  def __str__(self):
    return self.fullname()
    
  def get_absolute_url(self):
    return reverse('parishioner-view')
  
  def fullname(self):
    return f'{self.title} {self.first_name} {self.middle_name} {self.surname}'
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    img = Image.open(self.passport.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.passport.path)
    
class PiousSocietyInfo(models.Model):
  parishioner = models.ForeignKey(Parishioner, on_delete=models.CASCADE)
  pious_society = models.ForeignKey(PiousSociety, on_delete=models.CASCADE, related_name='parishioner_status')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.parishioner} is {self.status} in {self.pious_society}'

class LayApostolateInfo(models.Model):
  parishioner = models.ForeignKey(Parishioner, on_delete=models.CASCADE)
  lay_apostolate = models.ForeignKey(LayApostolate, on_delete=models.CASCADE, related_name='parishioner_status')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.parishioner} is {self.status} in {self.lay_apostolate}'

class OtherGroupInfo(models.Model):
  parishioner = models.ForeignKey(Parishioner, on_delete=models.CASCADE)
  other_group = models.ForeignKey(OtherGroup, on_delete=models.CASCADE, related_name='parishioner_status')
  status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=10)
  
  def __str__(self):
    return f'{self.parishioner} is {self.status} in {self.other_group}'
  
class DeathDetail(models.Model):
  parishioner = models.ForeignKey(Parishioner, on_delete=models.CASCADE, related_name='death_detail')
  died_on = models.DateField()
  buried_on = models.DateField(null=True, blank=True)
  buried_by = models.CharField(max_length=200, blank=True)
  buried_at = models.CharField(max_length=400, blank=True)
  
  def __str__(self):
    return f"{self.parishioner}'s death detail"
  