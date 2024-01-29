from django.db import models
from django.urls import reverse

class Setting(models.Model):
  reg_no_prefix = models.CharField(max_length=20, blank=True)
  reg_no_length = models.IntegerField(default=5)
  reg_no_start = models.IntegerField(default=1)
  church_logo = models.ImageField(upload_to='church', default='church_default.jfif')
  church_saint_logo = models.ImageField(upload_to='church', default='church_default.jfif')
  church_name = models.CharField(max_length=200)
  church_address = models.CharField(max_length=200)
  created_on = models.DateField()
  baptism_reg_no_prefix = models.CharField(max_length=20, blank=True)
  baptism_reg_no_length = models.IntegerField(default=5)
  baptism_reg_no_start = models.IntegerField(default=1)
  communion_reg_no_prefix = models.CharField(max_length=20, blank=True)
  communion_reg_no_length = models.IntegerField(default=5)
  communion_reg_no_start = models.IntegerField(default=1)
  confirmation_reg_no_prefix = models.CharField(max_length=20, blank=True)
  confirmation_reg_no_length = models.IntegerField(default=5)
  confirmation_reg_no_start = models.IntegerField(default=1)
  matrimony_reg_no_prefix = models.CharField(max_length=20, blank=True)
  matrimony_reg_no_length = models.IntegerField(default=5)
  matrimony_reg_no_start = models.IntegerField(default=1)
  email_port = models.IntegerField(default=582)
  email_password = models.CharField(max_length=100, blank=True)
  email_username = models.CharField(max_length=100, blank=True)
  email_server = models.CharField(max_length=100, blank=True)
  
  def __str__(self):
    return f'settings for {self.church_name}'
  
  # class Meta:
  #   permissions = [
  #     ('codename', 'verbose name'),
  #   ]
