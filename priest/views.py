from django.shortcuts import render, HttpResponse, reverse, redirect, get_object_or_404
from .models import Priest
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


class PriestView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Priest
  permission_required = 'priest.view_priest'

class PriestCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = Priest
  fields = ('name', 'email', 'phone_number', 'type', 'passport', 'date_of_birth', 'date_ordained', 'date_resumed', 'date_transfered')
  permission_required = 'priest.add_priest'
  success_message = 'Priest record successfully created'

class PriestUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Priest
  fields = ('name', 'email', 'phone_number', 'type', 'passport', 'date_of_birth', 'date_ordained', 'date_resumed', 'date_transfered')
  permission_required = 'priest.change_priest'
  success_message = 'Priest record updated successfully'

class PriestDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Priest
  permission_required = 'priest.view_priest'

@login_required
@permission_required('priest.delete_priest')
def delete_priest(request, pk):
  priest = get_object_or_404(Priest, pk=pk)
  try:
    priest.delete()
  except Exception as e:
    # raise e
    print(e)
    return HttpResponse('error')
  return HttpResponse('success')