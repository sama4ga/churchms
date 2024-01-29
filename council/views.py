from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .models import Council, StationCouncil, CouncilHead
from station.models import Station
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CouncilListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Council
  permission_required = 'council.view_council'

class CouncilCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = Council
  fields = ('name', 'station',)
  permission_required = 'council.add_council'
  success_message = 'Council successfully created'

class CouncilUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Council
  fields = ('name', 'station',)
  permission_required = 'council.change_council'
  success_message = "Council successfully updated"

@login_required
@permission_required('council.delete_council')
def delete_council(request, pk):
  council = get_object_or_404(Council, pk=pk)
  council.delete()
  return HttpResponse('success')

@login_required
@permission_required('council.change_council')
def remove_station(request, pk, id):
  council = get_object_or_404(Council, pk=pk)
  station = get_object_or_404(Station, pk=id)
  council.station.remove(station)
  return HttpResponse('success')
  
class CouncilHeadCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = CouncilHead
  fields = ('council', 'position')
  permission_required = 'council.add_councilhead'
  success_message = 'Council head successfully added'
  
  def form_valid(self, form):
    form.instance.head_id = self.request.POST.get('head')
    return super().form_valid(form)

class CouncilHeadUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = CouncilHead
  fields = ('council', 'position')
  permission_required = 'council.change_councilhead'
  success_message = 'Council head successfully updated'
  
  def form_valid(self, form):
    form.instance.head_id = self.request.POST.get('head')
    return super().form_valid(form)
  
class CouncilHeadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = CouncilHead
  permission_required = 'council.view_councilhead'

@login_required
@permission_required('council.delete_councilhead')
def delete_councilhead(request, pk):
  councilhead = get_object_or_404(CouncilHead, pk=pk)
  councilhead.delete()
  return HttpResponse('success')
