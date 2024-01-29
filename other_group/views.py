from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from .models import OtherGroup
from parishioner.models import Parishioner, OtherGroupInfo
from church.extras import Status
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from rest_framework import viewsets
from .serializers import OtherGroupSerializer
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OtherGroupViewSet(viewsets.ModelViewSet):
  serializer_class = OtherGroupSerializer
  queryset = OtherGroup.objects.all()

class OtherGroupView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = OtherGroup
  context_object_name = 'other_groups'
  permission_required = 'other_group.view_othergroup'

@login_required
@permission_required(['other_group.view_othergroup', 'parishioner.view_parishioner'], raise_exception=True)
def other_group_members(request, pk):
  other_group = get_object_or_404(OtherGroup, pk=pk)
  statuses = Status
  return render(request, 'other_group/othergroup_members.html', context={'other_group':other_group, 'statuses':statuses})

class OtherGroupMembersAddView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  template_name = 'other_group/othergroup_members_add.html'
  permission_required = ['other_group.view_othergroup', 'other_group.change_othergroup', 'parishioner.view_parishioner', 'parishioner.change_parishioner']
  
  def post(self, request, pk):
    other_group = get_object_or_404(OtherGroup, pk=pk)
    for id in request.POST.getlist('ids'):
      parishioner = get_object_or_404(Parishioner, id=id)
      parishioner.other_group.add(other_group)
      parishioner.modified_by = request.user
      parishioner.save()
    messages.success(request, 'Member(s) successfully added')
    return redirect(reverse('other_group-members', kwargs={'pk':pk}))

  def get_queryset(self):
    return None

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    other_group = get_object_or_404(OtherGroup, pk=self.kwargs['pk'])
    context['other_group'] = other_group
    return context

@login_required
@permission_required(['other_group.view_othergroup', 'other_group.change_othergroup', 'parishioner.view_parishioner', 'parishioner.change_parishioner'], raise_exception=True)
def other_group_members_remove(request, pk, id):
  parishioner = get_object_or_404(Parishioner, id=id)
  other_group = get_object_or_404(OtherGroup, pk=pk)
  parishioner.other_group.remove(other_group)
  parishioner.modified_by = request.user
  parishioner.save()
  messages.success(request, 'Member successfully removed')
  return redirect(reverse("other_group-members", kwargs={'pk':pk}))

@login_required
@permission_required(['other_group.view_othergroup', 'other_group.change_othergroup'], raise_exception=True)  
def other_group_members_update_status(request):
  othergroupinfo = OtherGroupInfo.objects.filter(other_group__id=request.GET.get('pk'), parishioner__id=request.GET.get('id')).first()
  othergroupinfo.status = request.GET.get('status')
  othergroupinfo.save()
  return HttpResponse('success')
  
class OtherGroupCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
  model = OtherGroup
  fields = ['name', 'short_name', 'slogan']
  success_message = 'Other Group successfully created'
  permission_required = 'other_group.add_othergroup'
  
class OtherGroupUpdateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = OtherGroup
  fields = ['name', 'short_name', 'slogan']
  success_message = 'Other Group successfully updated'
  permission_required = 'other_group.change_othergroup'

@login_required
@permission_required('other_group.delete_othergroup', raise_exception=True)
def delete_other_group(request, pk):
  if request.method == "GET":
    other_group = get_object_or_404(OtherGroup, pk=pk)
    other_group.delete()
    return HttpResponse("success")

