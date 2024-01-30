from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from parishioner.models import Parishioner
from setting.models import Setting
from baptism.models import Baptism
from communion.models import Communion
from confirmation.models import Confirmation
from matrimony.models import Matrimony
from pious_society.models import PiousSociety
from lay_apostolate.models import LayApostolate
from other_group.models import OtherGroup
from station.models import Station
from organisation.models import Organisation
from .models import Event
from django.http import JsonResponse


def edit(request, pk):
  if not request.user.is_staff:
    raise PermissionDenied

def home(request):
  context = {}
  parishioners = Parishioner.objects.exclude(status='Deleted')
  living_parishioners = parishioners.exclude(status='Dead').count()
  baptised_parishioners = parishioners.filter(baptised=True).count()
  communicant_parishioners = parishioners.filter(communicant=True).count()
  confirmed_parishioners = parishioners.filter(confirmed=True).count()
  wedded_parishioners = parishioners.filter(wedded=True).count()

  if living_parishioners > 0:
    context['baptised_parishioners_perc'] = round((baptised_parishioners/living_parishioners)*100,2)
    context['communicant_parishioners_perc'] = round((communicant_parishioners/living_parishioners)*100,2)
    context['confirmed_parishioners_perc'] = round((confirmed_parishioners/living_parishioners)*100,2)
    context['wedded_parishioners_perc'] = round((wedded_parishioners/living_parishioners)*100,2)
  else:
    context['baptised_parishioners_perc'] = 0
    context['communicant_parishioners_perc'] = 0
    context['confirmed_parishioners_perc'] = 0
    context['wedded_parishioners_perc'] = 0

  context['active_parishioners'] = parishioners.filter(status='Active').count()
  context['inactive_parishioners'] = parishioners.filter(status='Inactive').count()
  context['suspended_parishioners'] = parishioners.filter(status='Suspended').count()
  context['domiciled_parishioners'] = parishioners.filter(status='Domiciled').count()
  context['probation_parishioners'] = parishioners.filter(status='Probation').count()
  context['dead_parishioners'] = parishioners.filter(status='Dead').count()
  context['communicant_parishioners'] = communicant_parishioners
  context['confirmed_parishioners'] = confirmed_parishioners
  context['baptised_parishioners'] = baptised_parishioners
  context['wedded_parishioners'] = wedded_parishioners
  context['parishioners_count'] = parishioners.count()
  context['setting'] = Setting.objects.first()
  context['baptism_record'] = Baptism.objects.count()
  context['communion_record'] = Communion.objects.count()
  context['confirmation_record'] = Confirmation.objects.count()
  context['matrimony_record'] = Matrimony.objects.count()
  context['pious_society_record'] = PiousSociety.objects.count()
  context['lay_apostolate_record'] = LayApostolate.objects.count()
  context['other_group_record'] = OtherGroup.objects.count()
  context['station_record'] = Station.objects.count()
  context['organisation_record'] = Organisation.objects.count()
  return render(request, 'church/home.html', context=context)

class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Event
  permission_required = 'church.view_event'

class EventDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Event
  permission_required = 'church.view_event'

class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
  model = Event
  fields = ('title', 'description', 'start', 'end', 'color', 'allDay', 'event_type', 'url')
  permission_required = 'church.add_event'
  success_message = "Event successfully created"

class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
  model = Event
  fields = ('title', 'description', 'start', 'end', 'color', 'allDay', 'event_type', 'url')
  permission_required = 'church.update_event'
  success_message = "Event successfully updated"

@login_required
@permission_required('church.view_event', raise_exception=True)
def get_events(request):
  events = Event.objects.all()
  return HttpResponse(JsonResponse(list(events.values()), safe=False))

@login_required
@permission_required('church.view_event', raise_exception=True)
def view_event(request, pk):
  event = get_object_or_404(Event, pk=pk)
  return HttpResponse(event)

@login_required
@permission_required('church.add_event', raise_exception=True)
def create_event(request):
  print(request.GET.get('start'))
  print(request.GET.get('end'))
  event = Event.objects.create(
    title=request.GET.get('title'),
    description=request.GET.get('description'),
    start=request.GET.get('start'),
    end=request.GET.get('end'),
    color=request.GET.get('color'),
    allDay=request.GET.get('allDay')
  )
  # event.url = reverse('calendar-view-event', kwargs={'pk':event.id})
  # event.save()
  return HttpResponse('success')

@login_required
@permission_required('church.update_event', raise_exception=True)
def update_event(request, pk):
  print(request.GET.get('start'))
  print(request.GET.get('end'))
  event = get_object_or_404(Event, pk=pk)
  event.title=request.GET.get('title')
  event.description=request.GET.get('description')
  event.start=request.GET.get('start')
  event.end=request.GET.get('end')
  event.color=request.GET.get('color')
  event.allDay=request.GET.get('allDay')
  event.save()
  return HttpResponse('success')

@login_required
@permission_required('church.delete_event', raise_exception=True)
def delete_event(request, pk):
  event = get_object_or_404(Event, pk=pk)
  event.delete()
  return HttpResponse('success')
