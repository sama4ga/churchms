from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from .models import Baptism
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
from .serializers import BaptismSerializer, BaptismSerializer1


class BaptismDataTableViewSet(viewsets.ModelViewSet):
  serializer_class = BaptismSerializer1
  queryset = Baptism.objects.all().prefetch_related()
  
  def filter_for_datatable(self, queryset):
    
    search_query = self.request.query_params.get('search[value]')
    if search_query:
      queryset = queryset.filter(
        Q(candidate__surname__icontains=search_query) | Q(candidate__first_name__icontains=search_query) | Q(candidate__middle_name__icontains=search_query) | Q(minister__name__icontains=search_query) | Q(sponsor__icontains=search_query) | Q(date__icontains=search_query)
        )
    
    ordering_column = self.request.query_params.get('order[0][column]')
    ordering_direction = self.request.query_params.get('order[0][dir]')
    ordering = None
    if ordering_column == '0':
      ordering = 'candidate'
    if ordering_column == '1':
      ordering = 'minister'
    if ordering_column == '2':
      ordering = 'sponsor'
    if ordering_column == '3':
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
    
class BaptismViewSet(viewsets.ModelViewSet):
  serializer_class = BaptismSerializer
  queryset = Baptism.objects.all().prefetch_related()

class BaptismView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Baptism
  permission_required = 'baptism.view_baptism'

class BaptismCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = Baptism
  fields = ('minister', 'sponsor', 'date',)
  permission_required = 'baptism.add_baptism'
  success_message = 'Record successfully created'
  
  def form_valid(self, form):
    form.instance.candidate_id = self.request.POST.get('candidate')
    return super().form_valid(form)

class BaptismUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Baptism
  fields = ('minister', 'sponsor', 'date',)
  permission_required = 'baptism.change_baptism'
  success_message = 'Record successfully updated'
  
  def form_valid(self, form):
    form.instance.candidate_id = self.request.POST.get('candidate')
    return super().form_valid(form)
  
class BaptismDetailView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Baptism
  permission_required = 'baptism.view_baptism'
  
@login_required
@permission_required('baptism.delete_baptism', raise_exception=True)
def delete_record(request, pk):
  record = get_object_or_404(Baptism, pk=pk)
  record.delete()
  return HttpResponse('success')