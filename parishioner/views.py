from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Parishioner, DeathDetail
from organisation.models import Organisation, OrganisationInfo
from society.models import WorkingSociety
from station.models import Station
from setting.models import Setting
from church.extras import Status
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import generics
from .serializers import ParishionerSerializer, DeathDetailSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.core import serializers
# from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

# generics.ListAPIView
class ParishionerDataTableViewSet(viewsets.ModelViewSet):
  serializer_class = ParishionerSerializer
  queryset = Parishioner.objects.all().prefetch_related()
  
  def filter_for_datatable(self, queryset):
    # filtering
    search_query = self.request.query_params.get('search[value]')
    if search_query:
      # queryset = queryset.annotate(
      #   search=SearchVector('first_name','surname','middle_name')
      # ).filter(search=search_query)
      queryset = queryset.filter(
        Q(first_name__icontains=search_query) | Q(middle_name__icontains=search_query) | Q(surname__icontains=search_query)
        )
    # ordering
    ordering_column = self.request.query_params.get('order[0][column]')
    ordering_direction = self.request.query_params.get('order[0][dir]')
    ordering = None
    if ordering_column == '0':
      ordering = 'first_name'
    if ordering_column == '1':
      ordering = 'first_name'
    if ordering and ordering_direction == 'desc':
      ordering = f"-{ordering}"
    if ordering:
      queryset = queryset.order_by(ordering)
    return queryset
    
  def list(self, request, *args, **kwargs):
    draw = request.query_params.get('draw')
    queryset = self.filter_queryset(self.get_queryset())
    
    if(request.query_params.get('station_id') != None and request.query_params.get('station_id') != ""):
      queryset = queryset.filter(station_id=request.query_params.get('station_id'))
    
    if(request.query_params.get('organisation_id') != None and request.query_params.get('organisation_id') != ""):
      queryset = queryset.filter(organisation__organisation_id=request.query_params.get('organisation_id'))
    
    if(request.query_params.get('society_id') != None and request.query_params.get('society_id') != ""):
      queryset = queryset.filter(working_society_id=request.query_params.get('society_id'))
    
    if(request.query_params.get('baptised') != None and request.query_params.get('baptised') != ""):
      queryset = queryset.filter(baptised=request.query_params.get('baptised'))

    if(request.query_params.get('communicant') != None and request.query_params.get('communicant') != ""):
      queryset = queryset.filter(communicant=request.query_params.get('communicant'))

    if(request.query_params.get('confirmed') != None and request.query_params.get('confirmed') != ""):
      queryset = queryset.filter(confirmed=request.query_params.get('confirmed'))

    if(request.query_params.get("wedded") != None and request.query_params.get("wedded") != ""):
      queryset = queryset.filter(wedded=request.query_params.get('wedded'))
    
    # add_members is used specify that the request is made using the add member button, thus members of that group should be excluded
    if(request.query_params.get("add_members") != None): 
      if request.query_params.get('pious_society_id') != None:
        queryset = queryset.exclude(pious_society__id=request.query_params.get('pious_society_id'))
      elif request.query_params.get('other_group_id') != None:
        queryset = queryset.exclude(other_group__id=request.query_params.get('other_group_id'))
      elif request.query_params.get('lay_apostolate_id') != None:
        queryset = queryset.exclude(lay_apostolate__id=request.query_params.get('lay_apostolate_id'))
    else:
      if(request.query_params.get("pious_society_id") != None and request.query_params.get("pious_society_id") != ''):
        queryset = queryset.filter(pious_society__id=request.query_params.get('pious_society_id'))
      if(request.query_params.get("other_group_id") != None and request.query_params.get("other_group_id") != ''):
        queryset = queryset.filter(other_group__id=request.query_params.get('other_group_id'))
      if(request.query_params.get("lay_apostolate_id") != None and request.query_params.get("lay_apostolate_id") != ''):
        queryset = queryset.filter(lay_apostolate__id=request.query_params.get('lay_apostolate_id'))
    # print(queryset)
    if(request.query_params.get('status') != None and request.query_params.get('status') != ""):
      status = request.query_params.get('status')
      # parishioner is used to specify that the parishioner status query should be at the parish level otherwise on the group level
      if request.query_params.get('parishioner') == None:
        if request.query_params.get('pious_society_id') != None:
          queryset = queryset.filter( pioussocietyinfo__pious_society__id=request.query_params.get('pious_society_id'), pioussocietyinfo__status=status)
        if request.query_params.get('other_group_id') != None:
          queryset = queryset.filter(othergroupinfo__other_group__id=request.query_params.get('other_group_id'), othergroupinfo__status=status)
        if request.query_params.get('lay_apostolate_id') != None:
          queryset = queryset.filter(layapostolateinfo__lay_apostolate__id=request.query_params.get('lay_apostolate_id'), layapostolateinfo__status=status)
        if request.query_params.get('working_society_id') != None:
          queryset = queryset.filter(working_society_status=status)
        if request.query_params.get('station_id') != None:
          queryset = queryset.filter(station_status=status)
        if request.query_params.get('organisation_id') != None:
          queryset = queryset.filter(organisation_status=status)
      else:
        queryset = queryset.filter(status=status)
    # print(queryset, request.query_params.get('status'))
    # exclude deleted members unless requested
    if request.query_params.get('deleted') == None:
      queryset = queryset.filter(~Q(status='Deleted'))
      
    # exclude dead parishioners unless requeseted
    if request.query_params.get('dead') == None:
      queryset = queryset.filter(~Q(status='Dead'))
    # print(queryset)
    recordsTotal = queryset.count()
    filtered_queryset = self.filter_for_datatable(queryset)
    try:
        start = int(request.query_params.get('start'))
    except ValueError:
        start = 0
    try:
        length = int(request.query_params.get('length'))
    except ValueError:
        length = 100
    end = length + start
    if length == -1:
      serializer = self.get_serializer(filtered_queryset, many=True)
    else:
      serializer = self.get_serializer(filtered_queryset[start:end], many=True)
    response = {
        'draw': draw,
        'recordsTotal': recordsTotal,
        'recordsFiltered': filtered_queryset.count(),
        'data': serializer.data
    }
    return JsonResponse(response)
    
class ParishionerViewSet(viewsets.ModelViewSet):
  serializer_class = ParishionerSerializer
  queryset = Parishioner.objects.all().prefetch_related()

class DeathDetailViewSet(viewsets.ModelViewSet):
  serializer_class = DeathDetailSerializer
  queryset = DeathDetail.objects.all().prefetch_related()
  
@login_required
@permission_required('parishioner.view_parishioner', raise_exception=True)
def list_parishioner(request):
  organisations = Organisation.objects.all()
  stations = Station.objects.all()
  societies = WorkingSociety.objects.all()
  statuses = Status
  context = {
    'organisations' :  organisations,
    'stations' : stations,
    'societies' : societies,
    'statuses' : statuses
  }
  
  return render(request, 'parishioner/parishioner_list.html', context = context)

class ParishionerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Parishioner
  context_object_name = 'parishioner'
  permission_required = 'parishioner.view_parishioner'

class ParishionerCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
  model = Parishioner
  fields = ['title', 'surname', 'first_name', 'middle_name', 'phone_number', 'occupation', 'residential_address', 'home_address', 'office_address', 'diocese_of_origin', 'parish_of_origin', 'state_of_origin', 'lga_of_origin', 'email', 'passport', 'marital_status', 'gender', 'date_of_birth', 'spouse_name', 'station', 'organisation', 'working_society', 'pious_society', 'other_group', 'lay_apostolate', 'baptised', 'communicant', 'confirmed', 'wedded', 'charisma']
  success_message = 'Parishioner successfully created'
  permission_required = 'parishioner.add_parishioner'
  
  def form_valid(self, form):
    form.instance.created_by = self.request.user
    form.instance.modified_by = self.request.user
    return super().form_valid(form)
  
class ParishionerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
  model = Parishioner
  fields = ['title', 'surname', 'first_name', 'middle_name', 'phone_number', 'occupation', 'residential_address', 'home_address', 'office_address', 'diocese_of_origin', 'parish_of_origin', 'state_of_origin', 'lga_of_origin', 'email', 'passport', 'marital_status', 'gender', 'date_of_birth', 'spouse_name', 'station', 'organisation', 'working_society', 'pious_society', 'other_group', 'lay_apostolate', 'baptised', 'communicant', 'confirmed', 'wedded', 'charisma']
  success_message = 'Parishioner successfully updated'
  permission_required = 'parishioner.change_parishioner'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    instance = self.get_object()
    organisations = OrganisationInfo.objects.filter(station_id=instance.station_id)
    societies = WorkingSociety.objects.filter(organisation_id=instance.organisation_id)
    context['organisations'] = organisations
    context['societies'] = societies
    return context

  def form_valid(self, form):
    form.instance.modified_by = self.request.user
    return super().form_valid(form)
  
@login_required
@permission_required('parishioner.delete_parishioner', raise_exception=True)
def delete_parishioner(request, pk):
  if request.method == "GET":
    parishioner = get_object_or_404(Parishioner, pk=pk)
    parishioner.status = 'Deleted'
    parishioner.deleted_on = timezone.now()
    parishioner.deleted_by = request.user
    parishioner.save()
    # parishioner.delete()
    return HttpResponse("success")

def delete_parishioner_multi(request):
  for id in request.GET.getlist('ids'):
    parishioner = get_object_or_404(Parishioner, id=id)
    parishioner.status = 'Deleted'
    parishioner.deleted_on = timezone.now()
    parishioner.deleted_by = request.user
    parishioner.save()
  return HttpResponse('success')

def get_organisation_by_station(request):
  organisation = OrganisationInfo.objects.filter(station_id=request.GET['id'])
  return HttpResponse(JsonResponse(list(organisation.values('id', 'organisation','organisation__short_name', 'station', 'station__name')), safe=False))

def get_working_society_by_organisation(request):
  society = WorkingSociety.objects.filter(organisation_id=request.GET['id'])
  return HttpResponse(JsonResponse(list(society.values()), safe=False))

@login_required
@permission_required('parishioner.change_parishioner', raise_exception=True)
def update_status(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  parishioner.status = request.GET.get('status')
  parishioner.modified_by = request.user
  parishioner.save()
  return HttpResponse('success')

def update_status_multi(request):
  for id in request.GET.getlist('ids'):
    parishioner = get_object_or_404(Parishioner, id=id)
    parishioner.status = request.GET.get('status')
    parishioner.modified_by = request.user
    parishioner.save()
  return HttpResponse('success')

@login_required
@permission_required(['parishioner.change_parishioner', 'parishioner.add_deathdetail'], raise_exception=True)
def mark_dead(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  parishioner.status = 'Dead'
  parishioner.modified_by = request.user
  parishioner.save()
  DeathDetail.objects.create(parishioner=parishioner, died_on=request.GET.get('died_on'), buried_on=request.GET.get('buried_on'), buried_by=request.GET.get('buried_by'), buried_at=request.GET.get('buried_at'))
  return HttpResponse('success')

@login_required
@permission_required(['parishioner.view_deathdetail', 'parishioner.view_parishioner'], raise_exception=True)
def get_death_register(request):
  organisations = Organisation.objects.all()
  stations = Station.objects.all()
  societies = WorkingSociety.objects.all()
  context = {
    'organisations' :  organisations,
    'stations' : stations,
    'societies' : societies
  }
  return render(request, 'parishioner/dead_parishioner.html', context=context)

@login_required
@permission_required(['parishioner.change_deathdetail', 'parishioner.change_parishioner'], raise_exception=True)
def update_death_detail(request):
  death_detail = get_object_or_404(DeathDetail, parishioner__id=request.GET.get('parishioner_id'))
  death_detail.died_on=request.GET.get('died_on')
  death_detail.buried_on=request.GET.get('buried_on')
  death_detail.buried_by=request.GET.get('buried_by')
  death_detail.buried_at=request.GET.get('buried_at')
  death_detail.save()
  return HttpResponse('success')
  
@login_required
@permission_required(['parishioner.delete_deathdetail', 'parishioner.delete_parishioner'], raise_exception=True)
def delete_dead_parishioners(request):
  Parishioner.objects.filter(status='Dead').delete()
  return HttpResponse('success')

@login_required
@permission_required(['parishioner.delete_deathdetail', 'parishioner.delete_parishioner'], raise_exception=True)
def delete_dead_parishioner(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  try:
    parishioner.delete()
  except Exception as e:
    # raise e
    print(e)
    return HttpResponse('error')
  return HttpResponse('success')

@login_required
@permission_required(['parishioner.delete_deathdetail', 'parishioner.change_parishioner'], raise_exception=True)
def remove_dead_parishioners(request):
  for parishioner in Parishioner.objects.filter(status='Dead'):
    parishioner.status = 'Active'
    parishioner.modified_by = request.user
    parishioner.save()
  DeathDetail.objects.all().delete()
  return HttpResponse('success')

@login_required
@permission_required(['parishioner.delete_deathdetail', 'parishioner.change_parishioner'], raise_exception=True)
def mark_alive(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  parishioner.status = 'Active'
  parishioner.modified_by = request.user
  parishioner.save()
  DeathDetail.objects.filter(parishioner=parishioner).delete()
  return HttpResponse('success')
  
@login_required
@permission_required(['parishioner.view_deathdetail', 'parishioner.view_parishioner'], raise_exception=True)
def get_death_detail(request):
  death_detail = DeathDetail.objects.filter(parishioner__id=request.GET.get('parishioner_id'))
  return HttpResponse(JsonResponse(list(death_detail.values()), safe=False))
  # death_detail = serializers.serialize('json', death_detail)
  # return HttpResponse(death_detail, content_type="text/json-comment-filtered")

@login_required
@permission_required(['parishioner.view_parishioner', 'parishioner.view_deathdetail'], raise_exception=True)
def get_deleted_parishioners(request):
  organisations = Organisation.objects.all()
  stations = Station.objects.all()
  societies = WorkingSociety.objects.all()
  context = {
    'organisations' :  organisations,
    'stations' : stations,
    'societies' : societies
  }
  return render(request, 'parishioner/deleted_parishioner.html', context=context)

@login_required
@permission_required('parishioner.delete_parishioner', raise_exception=True)
def remove_deleted_parishioners(request):
  try:
    Parishioner.objects.filter(status='Deleted').delete()
  except Exception as e:
    # raise e
    print(e)
    return HttpResponse('error')
  return HttpResponse('success')

@login_required
@permission_required('parishioner.delete_parishioner', raise_exception=True)
def remove_deleted_parishioner(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  try:
    parishioner.delete()
  except Exception as e:
    # raise e
    print(e)
    return HttpResponse('error')
  return HttpResponse('success')

@login_required
@permission_required('parishioner.change_parishioner', raise_exception=True)
def restore_deleted_parishioner(request):
  parishioner = get_object_or_404(Parishioner, id=request.GET.get('id'))
  parishioner.status = 'Active'
  parishioner.died_on = None
  parishioner.buried_on = None
  parishioner.buried_at = ''
  parishioner.buried_by = ''
  parishioner.modified_by = request.user
  parishioner.save()
  return HttpResponse('success')

@login_required
@permission_required('parishioner.change_parishioner', raise_exception=True)
def restore_deleted_parishioners(request):
  for parishioner in Parishioner.objects.filter(status='Deleted'):
    parishioner.status = 'Active'
    parishioner.died_on = None
    parishioner.buried_on = None
    parishioner.buried_at = ''
    parishioner.buried_by = ''
    parishioner.modified_by = request.user
    parishioner.save()
  return HttpResponse('success')

@login_required
@permission_required(['baptism.view_baptism', 'communion.view_communion', 'confirmation.view_confirmation', 'matrimony.view_matrimony'], raise_exception=True)
def sacrament_card(request):
  context = {}
  if request.method == "POST":
    parishioner = get_object_or_404(Parishioner, pk=request.POST.get('pk'))
    context['parishioner'] = parishioner
  return render(request, 'parishioner/sacrament_card.html', context=context)

@login_required
@permission_required('matrimony.view_matrimony', raise_exception=True)
def marriage_certificate(request):
  context = {}
  if request.method == "POST":
    parishioner = get_object_or_404(Parishioner, pk=request.POST.get('pk'))
    if parishioner.gender == 'Male':
      context['records'] = parishioner.grooms.all
    else:
      context['records'] = parishioner.brides.all
      
    context['setting'] = Setting.objects.first()
  return render(request, 'parishioner/marriage_certificate.html', context=context)

def get_positions_held(request, pk):
  parishioner = get_object_or_404(Parishioner, pk=pk)
  return HttpResponse(JsonResponse(list(parishioner.values('id', 'positions__council__name', 'positions__council__id', 'positions__status','positions__position')), safe=False))

# config = dict(globals(  ))   #{}
# execfile('userconfig', config)
# background_color = config.get('background_color', 'black')
# foreground_color = config.get('foreground_color', 'white')