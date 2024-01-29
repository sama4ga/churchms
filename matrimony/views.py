from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from .models import Matrimony
from parishioner.models import Parishioner
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from rest_framework import viewsets
from django.http import JsonResponse
from django.core import serializers
from .serializers import MatrimonySerializer, MatrimonySerializer1


class MatrimonyDataTableViewSet(viewsets.ModelViewSet):
  serializer_class = MatrimonySerializer1
  queryset = Matrimony.objects.all().prefetch_related()
  
  def filter_for_datatable(self, queryset):
    
    search_query = self.request.query_params.get('search[value]')
    if search_query:
      queryset = queryset.filter(
        Q(bride__surname__icontains=search_query) | Q(bride__first_name__icontains=search_query) | Q(bride__middle_name__icontains=search_query) | Q(groom__surname__icontains=search_query) | Q(groom__first_name__icontains=search_query) | Q(groom__middle_name__icontains=search_query) | Q(minister__name__icontains=search_query) | Q(sponsor__icontains=search_query) | Q(bride_parent__icontains=search_query) | Q(bride_village__icontains=search_query) | Q(groom_parent__icontains=search_query) | Q(groom_village__icontains=search_query) | Q(date__icontains=search_query)
        )
    
    ordering_column = self.request.query_params.get('order[0][column]')
    ordering_direction = self.request.query_params.get('order[0][dir]')
    ordering = None
    if ordering_column == '0':
      ordering = 'bride'
    if ordering_column == '1':
      ordering = 'bride_parent'
    if ordering_column == '2':
      ordering = 'bride_village'
    if ordering_column == '3':
      ordering = 'groom'
    if ordering_column == '4':
      ordering = 'groom_parent'
    if ordering_column == '5':
      ordering = 'groom_village'
    if ordering_column == '6':
      ordering = 'sponsor'
    if ordering_column == '7':
      ordering = 'minister'
    if ordering_column == '8':
      ordering = 'date'
    if ordering and ordering_direction == 'desc':
      ordering = f"-{ordering}"
    if ordering:
      queryset = queryset.order_by(ordering)
    return queryset
    
  def list(self, request, *args, **kwargs):
    draw = request.query_params.get('draw')
    queryset = self.filter_queryset(self.get_queryset())
    
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
    
class MatrimonyViewSet(viewsets.ModelViewSet):
  serializer_class = MatrimonySerializer
  queryset = Matrimony.objects.all().prefetch_related()

class MatrimonyView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Matrimony
  permission_required = 'matrimony.view_matrimony'

class MatrimonyCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = Matrimony
  fields = ('bride_parent', 'bride_village', 'groom_parent', 'groom_village', 'sponsor', 'sponsor_address', 'minister', 'date')
  permission_required = 'matrimony.add_matrimony'
  success_message = 'Record successfully created'

  def form_valid(self, form):
    form.instance.bride_id = self.request.POST.get('bride')
    form.instance.groom_id = self.request.POST.get('groom')
    return super().form_valid(form)
    
class MatrimonyUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Matrimony
  fields = ('bride_parent', 'bride_village', 'groom_parent', 'groom_village', 'sponsor', 'sponsor_address', 'minister', 'date')
  permission_required = 'matrimony.change_matrimony'
  success_message = 'Record successfully updated'
  
  def form_valid(self, form):
    form.instance.bride_id = self.request.POST.get('bride')
    form.instance.groom_id = self.request.POST.get('groom')
    return super().form_valid(form)
  
class MatrimonyDetailView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Matrimony
  permission_required = 'matrimony.view_matrimony'
  
@login_required
@permission_required('matrimony.delete_matrimony', raise_exception=True)
def delete_record(request, pk):
  record = get_object_or_404(Matrimony, pk=pk)
  record.delete()
  return HttpResponse('success')