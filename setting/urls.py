from django.urls import path
from . import views
from .forms import BaptismSettingForm, CommunionSettingForm, ConfirmationSettingForm, MatrimonySettingForm, EmailSettingForm

urlpatterns = [
    path('', views.setting, name='setting'),
    path('<int:pk>/general/', views.GeneralSettingView.as_view(), name='setting-general'),
    path('<int:pk>/email/', views.GeneralSettingView.as_view(form_class=EmailSettingForm), name='setting-email'),
    path('<int:pk>/baptism/', views.GeneralSettingView.as_view(form_class=BaptismSettingForm), name='setting-baptism'),
    path('<int:pk>/communion/', views.GeneralSettingView.as_view(form_class=CommunionSettingForm), name='setting-communion'),
    path('<int:pk>/confirmation/', views.GeneralSettingView.as_view(form_class=ConfirmationSettingForm), name='setting-confirmation'),
    path('<int:pk>/matrimony/', views.GeneralSettingView.as_view(form_class=MatrimonySettingForm), name='setting-matrimony'),
    path('permission/', views.PermissionsView.as_view(), name='setting-permission'),
    path('groups/', views.GroupsListView.as_view(), name='setting-groups'),
    path('groups/<int:pk>/permissions/', views.group_permissions, name='setting-group_permissions'),
]