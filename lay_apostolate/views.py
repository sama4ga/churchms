from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from .models import LayApostolate
from parishioner.models import Parishioner, LayApostolateInfo
from church.extras import Status
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from rest_framework import viewsets
from .serializers import LayApostolateSerializer
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LayApostolateViewSet(viewsets.ModelViewSet):
  serializer_class = LayApostolateSerializer
  queryset = LayApostolate.objects.all()

class LayApostolateView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = LayApostolate
  context_object_name = 'lay_apostolates'
  permission_required = 'lay_apostolate.view_layapostolate'

@login_required
@permission_required(['lay_apostolate.view_layapostolate', 'parishioner.view_parishioner'], raise_exception=True)
def lay_apostolate_members(request, pk):
  lay_apostolate = get_object_or_404(LayApostolate, pk=pk)
  statuses = Status
  return render(request, 'lay_apostolate/layapostolate_members.html', context={'lay_apostolate':lay_apostolate, 'statuses':statuses})

class LayApostolateMembersAddView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  template_name = 'lay_apostolate/layapostolate_members_add.html'
  permission_required = ['lay_apostolate.view_layapostolate', 'lay_apostolate.change_layapostolate', 'parishioner.view_parishioner', 'parishioner.change_parishioner']
  
  def post(self, request, pk):
    lay_apostolate = get_object_or_404(LayApostolate, pk=pk)
    for id in request.POST.getlist('ids'):
      parishioner = get_object_or_404(Parishioner, id=id)
      parishioner.lay_apostolate.add(lay_apostolate)
      parishioner.modified_by = request.user
      parishioner.save()
    messages.success(request, 'Member(s) successfully added')
    return redirect(reverse('lay_apostolate-members', kwargs={'pk':pk}))

  def get_queryset(self):
    return None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    lay_apostolate = get_object_or_404(LayApostolate, pk=self.kwargs['pk'])
    context['lay_apostolate'] = lay_apostolate
    return context

@login_required
@permission_required(['lay_apostolate.view_layapostolate', 'lay_apostolate.change_layapostolate', 'parishioner.view_parishioner', 'parishioner.change_parishioner'], raise_exception=True)
def lay_apostolate_members_remove(request, pk, id):
  parishioner = get_object_or_404(Parishioner, id=id)
  lay_apostolate = get_object_or_404(LayApostolate, pk=pk)
  parishioner.lay_apostolate.remove(lay_apostolate)
  parishioner.modified_by = request.user
  parishioner.save()
  messages.success(request, 'Member successfully removed')
  return redirect(reverse("lay_apostolate-members", kwargs={'pk':pk}))

@login_required
@permission_required(['lay_apostolate.view_layapostolate', 'lay_apostolate.change_layapostolate'], raise_exception=True)
def lay_apostolate_members_update_status(request):
  layapostolateinfo = LayApostolateInfo.objects.filter(lay_apostolate__id=request.GET.get('pk'), parishioner__id=request.GET.get('id')).first()
  layapostolateinfo.status = request.GET.get('status')
  layapostolateinfo.save()
  return HttpResponse('success')
  
class LayApostolateCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = LayApostolate
  fields = ['name', 'short_name', 'slogan']
  success_message = 'Lay Apostolate successfully created'
  permission_required = 'lay_apostolate.add_layapostolate'
  
class LayApostolateUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = LayApostolate
  fields = ['name', 'short_name', 'slogan']
  success_message = 'Lay Apostolate successfully updated'
  permission_required = 'lay_apostolate.change_layapostolate'

@login_required
@permission_required('lay_apostolate.delete_layapostolate', raise_exception=True)
def delete_lay_apostolate(request, pk):
  if request.method == "GET":
    lay_apostolate = get_object_or_404(LayApostolate, pk=pk)
    lay_apostolate.delete()
    return HttpResponse("success")

