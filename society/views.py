from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from .models import WorkingSociety
from station.models import Station
from organisation.models import OrganisationInfo
from parishioner.models import Parishioner
from church.extras import Status
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .serializers import WorkingSocietySerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class WorkingSocietyViewSet(viewsets.ModelViewSet):
  serializer_class = WorkingSocietySerializer
  queryset = WorkingSociety.objects.all()

class WorkingSocietyView(ListView):
  model = WorkingSociety
  context_object_name = 'working_societies'

@login_required
@permission_required(['parishioner.view_parishioner', 'society.view_workingsociety'], raise_exception=True)
def working_society_members(request, pk):
  society = get_object_or_404(WorkingSociety, pk=pk)
  return render(request, 'society/workingsociety_members.html', context={'society':society})

class WorkingSocietyMembersAddView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  context_object_name = 'parishioners'
  template_name = 'society/workingsociety_members_add.html'
  permission_required = ['parishioner.view_parishioner', 
  'parishioner.change_parishioner', 'society.view_workingsociety', 'society.change_workingsociety']
  
  def post(self, request, pk):
    working_society = get_object_or_404(WorkingSociety, pk=pk)
    for id in request.POST.getlist('ids'):
      parishioner = get_object_or_404(Parishioner, id=id)
      parishioner.working_society = working_society
      parishioner.modified_by = request.user
      parishioner.save()
    messages.success(request, 'Member(s) successfully added')
    return redirect(reverse('working_society-members', kwargs={'pk':pk}))

  def get_queryset(self):
    society = get_object_or_404(WorkingSociety, pk=self.kwargs['pk'])
    parishioners = Parishioner.objects.filter(organisation=society.organisation, working_society=None)
    return parishioners

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    society = get_object_or_404(WorkingSociety, pk=self.kwargs['pk'])
    context['society'] = society
    return context


class WorkingSocietyCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = WorkingSociety
  fields = ['name', 'organisation']
  success_message = 'Working Society successfully created'
  permission_required = 'society.add_workingsociety'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    station = Station.objects.all()
    context['stations'] = station
    return context

class WorkingSocietyUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = WorkingSociety
  fields = ['name', 'organisation']
  success_message = 'Working Society successfully updated'
  permission_required = 'society.change_workingsociety'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    instance = self.get_object()
    stations = Station.objects.all()
    organisations = OrganisationInfo.objects.filter(station_id=instance.organisation.station_id)
    context['stations'] = stations
    context['organisations'] = organisations
    context['org_id'] = instance.organisation.id
    return context

@login_required
@permission_required('society.delete_workingsociety', raise_exception=True)
def delete_working_society(request, pk):
  if request.method == "GET":
    working_society = get_object_or_404(WorkingSociety, pk=pk)
    working_society.delete()
    return HttpResponse("success")

@login_required
@permission_required(['society.view_workingsociety', 'society.change_workingsociety', 'parishioner.change_parishioner'], raise_exception=True)
def working_society_members_remove(request, pk, id):
  parishioner = get_object_or_404(Parishioner, id=id)
  parishioner.working_society = None
  parishioner.modified_by = request.user
  parishioner.save()
  messages.success(request, 'Member successfully removed')
  return redirect(reverse("working_society-members", kwargs={'pk':pk}))

@login_required
@permission_required(['parishioner.change_parishioner'], raise_exception=True)
def change_members_working_society(request):
  id = request.GET.get('id')
  parishioner = get_object_or_404(Parishioner, id=id)
  parishioner.working_society_id = request.GET.get('society_id')
  parishioner.modified_by = request.user
  parishioner.save()
  return HttpResponse('success')
