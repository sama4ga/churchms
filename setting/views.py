from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, resolve_url
from django.urls import reverse
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import Setting
from .forms import GeneralSettingForm, BaptismSettingForm, CommunionSettingForm, ConfirmationSettingForm, MatrimonySettingForm, EmailSettingForm
# from django.core.exceptions import PermissionDenied

class GeneralSettingView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
  queryset = Setting.objects.all()
  form_class = GeneralSettingForm
  success_message = "Setting updated successfully"
  # request.META.get('HTTP_REFERER') request.path_info request.build_absolute_url() request.get_full_path() request.path

  def get_success_url(self) -> str:
    return self.request.get_full_path()

  def test_func(self):
    return self.request.user.has_perms(['setting.view_setting', 'setting.change_setting'])

@login_required
@permission_required(['setting.view_setting', 'setting.change_setting'], raise_exception=True)
def setting(request):
  setting = Setting.objects.first()
  general_form = GeneralSettingForm(instance=setting)
  email_form = EmailSettingForm(instance=setting)
  baptism_form = BaptismSettingForm(instance=setting)
  communion_form = CommunionSettingForm(instance=setting)
  confirmation_form = ConfirmationSettingForm(instance=setting)
  matrimony_form = MatrimonySettingForm(instance=setting)

  if request.method == "POST":
    action = request.POST.get('action')
    if action == "church":
      form = GeneralSettingForm(request.POST, request.FILES, instance=setting)
    elif action == "email":
     form = EmailSettingForm(request.POST, instance=setting)
    elif action == "baptism":
      form = BaptismSettingForm(request.POST, instance=setting)
    elif action == "communion":
      form = CommunionSettingForm(request.POST, instance=setting)
    elif action == "confirmation":
      form = ConfirmationSettingForm(request.POST, instance=setting)
    elif action == "matrimony":
      form = MatrimonySettingForm(request.POST, instance=setting)
    
    status = update(request, form)
    if status:
      return redirect(reverse("setting"))
    else:
      if isinstance(form, GeneralSettingForm):
        general_form = form
      elif isinstance(form, EmailSettingForm):
        email_form = form
      elif isinstance(form, BaptismSettingForm):
        baptism_form = form
      elif isinstance(form, CommunionSettingForm):
        communion_form = form
      elif isinstance(form, ConfirmationSettingForm):
        confirmation_form = form
      elif isinstance(form, MatrimonySettingForm):
        matrimony_form = form

  return render(request, 'setting/setting.html', context={
    'general_form': general_form,
    'email_form': email_form,
    'baptism_form': baptism_form,
    'communion_form': communion_form,
    'confirmation_form': confirmation_form,
    'matrimony_form': matrimony_form
  })

def update(request, form):
  if form.is_valid():
    form.save()
    messages.success(request, 'Setting successfully updated')
    return True
  else:
    messages.error(request, 'Error while updating setting')
    return False

class PermissionsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  permission_required = ["setting.view_setting", "setting.change_setting"]
  template_name = 'setting/permission_form.html'
  model = Permission
  context_object_name = 'permissions'
    
class GroupsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  permission_required = ["setting.view_setting", "auth.view_group"]
  template_name = 'setting/group_list.html'
  model = Group
  context_object_name = 'groups'

@login_required
@permission_required(["setting.view_setting", "auth.view_permission", "auth.add_permission", "auth.change_permission"], raise_exception=True)
def group_permissions(request, pk):
  group = get_object_or_404(Group, pk=pk)
  permissions = Permission.objects.exclude(content_type__model__in=['logentry','profile','contenttype','organisationinfo',
                                                                    'layapostolateinfo','othergroupinfo','pioussocietyinfo',
                                                                    'session', 'stationcouncil'])
  if request.method == "POST":
    perms = []
    for perm in request.POST.getlist('permissions'):
      perms.append(perm)
    update_group_permissions(group, perms)
    messages.success(request, 'Permission successfully updated')
    return redirect(reverse('setting-group_permissions', kwargs={'pk':pk}))
  return render(request, 'setting/group_permission.html', context={'permissions':permissions, 'group':group})
  
# user.has_perm('foo.add_bar')
def update_group_permissions(group, permissions):
  group.permissions.clear()
  perms_to_add = permission_names_to_objects(permissions)
  group.permissions.add(*perms_to_add)

def permission_names_to_objects(names):
  """
  Given an iterable of permission names (e.g. 'app_label.add_model'),
  return an iterable of Permission objects for them.  The permission
  must already exist, because a permission name is not enough information
  to create a new permission.
  """
  result = []
  for name in names:
    app_label, codename = name.split(".", 1)
    try:
      result.append(Permission.objects.get(content_type__app_label=app_label,codename=codename))
    except Permission.DoesNotExist:
      # logger.exception("NO SUCH PERMISSION: %s, %s" % (app_label, codename))
      raise
  return result

# def get_all_perm_names_for_group(group):
#     # Return the set of permission names that the group should contain
#   pass

# def create_or_update_groups():
#   for group_name, perm_names in GROUP_PERMISSIONS.iteritems():
#     group, created = Group.objects.get_or_create(name=group_name)
#     perms_to_add = permission_names_to_objects(get_all_perm_names_for_group(group))
#     group.permissions.add(*perms_to_add)
#     if not created:
#       # Group already existed - make sure it doesn't have any perms we didn't want
#       to_remove = set(group.permissions.all()) - set(perms_to_add)
#       if to_remove:
#         group.permissions.remove(*to_remove)

# from django.db.models import get_models, get_app
# from django.contrib.auth.management import create_permissions

# apps = set([get_app(model._meta.app_label) for model in get_models()])
# for app in apps:
#   create_permissions(app, None, 2)
