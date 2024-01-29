from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from .models import PiousSociety
from parishioner.models import Parishioner, PiousSocietyInfo
from church.extras import Status
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from rest_framework import viewsets
from .serializers import PiousSocietySerializer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

class PiousSocietyViewSet(viewsets.ModelViewSet):
  serializer_class = PiousSocietySerializer
  queryset = PiousSociety.objects.all().prefetch_related()

class PiousSocietyView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = PiousSociety
  context_object_name = 'pious_societies'
  permission_required = 'pious_society.view_pioussociety'

@login_required
@permission_required(['pious_society.view_pioussociety', 'parishioner.view_parishioner'], raise_exception=True)
def pious_society_members(request, pk):
  pious_society = get_object_or_404(PiousSociety, pk=pk)
  statuses = Status
  return render(request, 'pious_society/pioussociety_members.html', context={'pious_society':pious_society, 'statuses':statuses})

class PiousSocietyMembersAddView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  template_name = 'pious_society/pioussociety_members_add.html'
  permission_required = ['pious_society.view_pioussociety', 'pious_society.change_pioussociety', 'parishioner.change_parishioner', 'parishioner.view_parishioner']
  
  def post(self, request, pk):
    pious_society = get_object_or_404(PiousSociety, pk=pk)
    for id in request.POST.getlist('ids'):
      parishioner = get_object_or_404(Parishioner, id=id)
      parishioner.pious_society.add(pious_society)
      parishioner.modified_by = request.user
      parishioner.save()
    messages.success(request, 'Member(s) successfully added')
    return redirect(reverse('pious_society-members', kwargs={'pk':pk}))

  def get_queryset(self):
    return None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pious_society = get_object_or_404(PiousSociety, pk=self.kwargs['pk'])
    context['pious_society'] = pious_society
    return context

@login_required
@permission_required(['pious_society.view_pioussociety', 'pious_society.change_pioussociety', 'parishioner.view_parishioner', 'parishioner.change_parishioner'], raise_exception=True)
def pious_society_members_remove(request, pk, id):
  parishioner = get_object_or_404(Parishioner, id=id)
  pious_society = get_object_or_404(PiousSociety, pk=pk)
  parishioner.pious_society.remove(pious_society)
  parishioner.modified_by = request.user
  parishioner.save()
  messages.success(request, 'Member successfully removed')
  return redirect(reverse("pious_society-members", kwargs={'pk':pk}))

@login_required
@permission_required(['pious_society.view_pioussociety', 'pious_society.change_pioussociety', 'parishioner.view_parishioner', 'parishioner.change_parishioner'], raise_exception=True)
def pious_society_members_update_status(request):
  pioussocietyinfo = PiousSocietyInfo.objects.filter(pious_society__id=request.GET.get('pk'), parishioner__id=request.GET.get('id')).first()
  pioussocietyinfo.status = request.GET.get('status')
  pioussocietyinfo.save()
  return HttpResponse('success')

class PiousSocietyCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = PiousSociety
  fields = ['name', 'slogan']
  success_message = 'Pious Society successfully created'
  permission_required = 'pious_society.add_pioussociety'
  
class PiousSocietyUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = PiousSociety
  fields = ['name', 'slogan']
  success_message = 'Pious Society successfully updated'
  permission_required = 'pious_society.change_pioussociety'

@login_required
@permission_required(['pious_society.delete_pioussociety'], raise_exception=True)
def delete_pious_society(request, pk):
  if request.method == "GET":
    pious_society = get_object_or_404(PiousSociety, pk=pk)
    pious_society.delete()
    return HttpResponse("success")

