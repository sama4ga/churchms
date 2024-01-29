from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Organisation, OrganisationInfo
from station.models import Station
from parishioner.models import Parishioner
from society.models import WorkingSociety
from church.extras import Status
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from .serializers import OrganisationSerializer, OrganisationInfoSerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OrganisationViewSet(viewsets.ModelViewSet):
  serializer_class = OrganisationSerializer
  queryset = Organisation.objects.all()

class OrganisationInfoViewSet(viewsets.ModelViewSet):
  serializer_class = OrganisationInfoSerializer
  queryset = OrganisationInfo.objects.all()

class OrganisationView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Organisation
  context_object_name = 'organisations'
  permission_required = 'organisation.view_organisation'

class OrganisationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Organisation
  context_object_name = 'organisation'
  permission_required = 'organisation.view_organisation'

class OrganisationCreateView(SuccessMessageMixin, LoginRequiredMixin,
PermissionRequiredMixin, CreateView):
  model = Organisation
  fields = ['name', 'short_name', 'slogan', 'station']
  success_message = 'Organisation successfully created'
  permission_required = 'organisation.add_organisation'

class OrganisationUpdateView(SuccessMessageMixin, LoginRequiredMixin,
PermissionRequiredMixin, UpdateView):
  model = Organisation
  fields = ['name', 'short_name', 'slogan', 'station']
  success_message = 'Organisation successfully updated'
  permission_required = 'organisation.change_organisation'

class OrganisationInfoView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  permission_required = 'organisation.view_organisation'
  def get_queryset(self):
    info = OrganisationInfo.objects.filter(organisation_id=self.kwargs['pk'])
    return info


class OrganisationInfoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = OrganisationInfo
  fields = ['meeting_days', 'meeting_days_suff', 'meeting_frequency']
  permission_required = 'organisation.change_organisation'

@login_required
@permission_required('organisation.delete_organisation', raise_exception=True)
def delete_organisation(request, pk):
  ''' deletes organisation from all stations '''
  if request.method == "GET":
    organisation = get_object_or_404(Organisation, pk=pk)
    organisation.delete()
    return HttpResponse("success")

@login_required
@permission_required('organisation.delete_organisation', raise_exception=True)
def remove_organisation(request, pk):
  ''' deletes organisation from a particular station '''
  organisation = get_object_or_404(OrganisationInfo, pk=pk)
  organisation.delete()
  return HttpResponse("success")

@login_required
@permission_required(['organisation.view_organisation', 'parishioner.view_parishioner'], raise_exception=True)
def organisation_members(request, pk):
  organisation = get_object_or_404(OrganisationInfo, pk=pk)
  societies = WorkingSociety.objects.filter(organisation_id=organisation.id)
  statuses = Status
  return render(request, 'organisation/stationorganisation_member.html', {
    'organisation':organisation,
    'societies':societies,
    'statuses':statuses
  })

@login_required
@permission_required(['organisation.view_organisation', 'parishioner.change_parishioner'], raise_exception=True)
def change_members_organisation(request):
  id = request.GET.get('id')
  parishioner = get_object_or_404(Parishioner, id=id)
  parishioner.organisation_id = request.GET.get('organisation_id')
  parishioner.working_society_id = request.GET.get('society_id')
  parishioner.modified_by = request.user
  parishioner.save()
  return HttpResponse('success')

def get_organisation_by_station(request):
  organisations = Organisation.objects.filter(station_id=request.GET['id'])
  return HttpResponse(JsonResponse(list(organisations.values('id','short_name','station__name')), safe=False))
  
def search_parishioner(request):
  if request.method == "POST":
    station_id = request.POST['cmbStation']
    if request.POST['cmbOrganisation']:
      organisation_id = request.POST['cmbOrganisation']
      parishioners = Parishioner.objects.filter(station_id=station_id, organisation_id=organisation_id)
    else:
      parishioners = Parishioner.objects.filter(station_id=station_id)
  elif request.method == "GET":
    name = request.GET['name']
    parishioners = Parishioner.objects.filter(surname__contains=name)
  return HttpResponse(parishioners)
