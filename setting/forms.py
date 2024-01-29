from django import forms
from .models import Setting

class EmailSettingForm(forms.ModelForm):
  """Form definition for EmailSetting."""
  email_password = forms.PasswordInput()
  class Meta:
    """Meta definition for EmailSettingform."""
    model = Setting
    fields = ('email_server', 'email_port', 'email_username', 'email_password')

class BaptismSettingForm(forms.ModelForm):
  """Form definition for EmailSetting."""

  class Meta:
    """Meta definition for EmailSettingform."""
    model = Setting
    fields = ('baptism_reg_no_prefix', 'baptism_reg_no_length', 'baptism_reg_no_start')

class CommunionSettingForm(forms.ModelForm):
  """Form definition for EmailSetting."""

  class Meta:
    """Meta definition for EmailSettingform."""
    model = Setting
    fields = ('communion_reg_no_prefix', 'communion_reg_no_length', 'communion_reg_no_start')

class ConfirmationSettingForm(forms.ModelForm):
  """Form definition for EmailSetting."""

  class Meta:
    """Meta definition for EmailSettingform."""
    model = Setting
    fields = ('confirmation_reg_no_prefix', 'confirmation_reg_no_length', 'confirmation_reg_no_start')

class MatrimonySettingForm(forms.ModelForm):
  """Form definition for MatrimonySetting."""

  class Meta:
    """Meta definition for MatrimonySettingform."""
    model = Setting
    fields = ('matrimony_reg_no_prefix', 'matrimony_reg_no_length', 'matrimony_reg_no_start')

class GeneralSettingForm(forms.ModelForm):
  """Form definition for EmailSetting."""

  class Meta:
    """Meta definition for EmailSettingform."""
    model = Setting
    fields = ('church_name', 'church_logo', 'church_saint_logo', 'created_on', 'reg_no_prefix',
            'reg_no_length', 'reg_no_length', 'reg_no_start')
