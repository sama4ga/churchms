from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from .models import Confirmation
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
from .serializers import ConfirmationSerializer, ConfirmationSerializer1


class ConfirmationDataTableViewSet(viewsets.ModelViewSet):
  serializer_class = ConfirmationSerializer1
  queryset = Confirmation.objects.all().prefetch_related()
  
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
    
class ConfirmationViewSet(viewsets.ModelViewSet):
  serializer_class = ConfirmationSerializer
  queryset = Confirmation.objects.all().prefetch_related()

class ConfirmationView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Confirmation
  permission_required = 'confirmation.view_confirmation'

class ConfirmationCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = Confirmation
  fields = ('minister', 'sponsor', 'date',)
  permission_required = 'confirmation.add_confirmation'
  success_message = 'Record successfully created'

  def form_valid(self, form):
    form.instance.candidate_id = self.request.POST.get('candidate')
    return super().form_valid(form)
    
class ConfirmationUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Confirmation
  fields = ('minister', 'sponsor', 'date',)
  permission_required = 'confirmation.change_confirmation'
  success_message = 'Record successfully updated'
  
  def form_valid(self, form):
    form.instance.candidate_id = self.request.POST.get('candidate')
    return super().form_valid(form)
    
class ConfirmationDetailView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Confirmation
  permission_required = 'confirmation.view_confirmation'
  
@login_required
@permission_required('confirmation.delete_confirmation', raise_exception=True)
def delete_record(request, pk):
  record = get_object_or_404(Confirmation, pk=pk)
  record.delete()
  return HttpResponse('success')