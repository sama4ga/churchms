from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Station
from organisation.models import OrganisationInfo
from parishioner.models import Parishioner
from society.models import WorkingSociety
from church.extras import Status
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .serializers import StationSerializer
from rest_framework import viewsets

class StationDataTableViewSet(viewsets.ModelViewSet):
  serializer_class = StationSerializer
  queryset = Station.objects.all()
  
class StationViewSet(viewsets.ModelViewSet):
  serializer_class = StationSerializer
  queryset = Station.objects.all()

class StationView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Station
  context_object_name = 'stations'
  permission_required = 'station.view_station'

class StationCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
  model = Station
  fields = ['name', 'address', 'date_created', 'picture']
  success_message = 'Station successfully created'
  permission_required = 'station.add_station'
  
class StationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
  model = Station
  fields = ['name', 'address', 'date_created', 'picture']
  success_message = 'Station successfully updated'
  permission_required = 'station.change_station'

def station_organisations(request, pk):
  ''' get orgainsations in a station '''
  organisations = OrganisationInfo.objects.filter(station_id=pk)
  return render(request, 'station/station_organisation_list.html', {'organisations':organisations})

@login_required
@permission_required('station.delete_station', raise_exception=True)
def delete_station(request, pk):
  if request.method == "GET":
    station = get_object_or_404(Station, pk=pk)
    station.delete()
    return HttpResponse("success")

class StationMembersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  context_object_name = 'station_members'
  template_name = 'station/station_members.html'
  permission_required = ['parishioner.view_parishioner']
  
  def get_queryset(self):
    station = get_object_or_404(Station, pk=self.kwargs['pk'])
    return station.members.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    station = get_object_or_404(Station, pk=self.kwargs['pk'])
    organisations = OrganisationInfo.objects.filter(station_id=station.id)
    societies = WorkingSociety.objects.filter(organisation__station_id=station.id)
    statuses = Status
    context['station'] = station
    context['organisations'] = organisations
    context['societies'] = societies
    context['statuses'] = statuses
    return context

@login_required
@permission_required('parishioner.change_parishioner', raise_exception=True)
def change_members_station(request):
  id = request.GET.get('id')
  parishioner = get_object_or_404(Parishioner, id=id)
  parishioner.station_id = request.GET.get('station_id')
  parishioner.organisation_id = request.GET.get('organisation_id')
  parishioner.working_society_id = request.GET.get('society_id')
  parishioner.save()
  return HttpResponse('success')
