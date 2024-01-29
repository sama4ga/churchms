from django.urls import path
from . import views

urlpatterns = [
  path('', views.list_parishioner, name='parishioner-view'),
  path('create/', views.ParishionerCreateView.as_view(), name='parishioner-create'),
  path('<int:pk>/', views.ParishionerDetailView.as_view(), name='parishioner-detail'),
  path('<int:pk>/update/', views.ParishionerUpdateView.as_view(), name='parishioner-update'),
  path('<int:pk>/delete/', views.delete_parishioner, name='parishioner-delete'),
  path('sacrament_card/', views.sacrament_card, name='parishioner-sacrament-card'),
  path('marriage_certificate/', views.marriage_certificate, name='parishioner-marriage-certificate'),
  path('update_status/', views.update_status, name='parishioner-update-status'),
  path('mark_dead/', views.mark_dead, name='parishioner-mark-dead'),
  path('death_register/', views.get_death_register, name='parishioner-death-register'),
  path('mark_alive/', views.mark_alive, name='parishioner-mark-alive'),
  path('dead/remove_all/', views.remove_dead_parishioners, name='parishioners-remove-dead'),
  path('dead/delete_all/', views.delete_dead_parishioners, name='parishioners-delete-dead'),
  path('dead/delete/', views.delete_dead_parishioner, name='parishioner-delete-dead'),
  path('death_detail/update/', views.update_death_detail, name='parishioner-update-death-detail'),
  path('get_death_detail/', views.get_death_detail, name='parishioner-get-death-detail'),
  path('deleted/', views.get_deleted_parishioners, name='parishioner-deleted'),
  path('deleted/restore', views.restore_deleted_parishioner, name='parishioner-restore'),
  path('deleted/restore_all', views.restore_deleted_parishioners, name='parishioners-restore'),
  path('deleted/delete_all', views.remove_deleted_parishioners, name='parishioners-delete-permanently'),
  path('deleted/delete', views.remove_deleted_parishioner, name='parishioner-delete-permanently'),
  path('station/organisation/', views.get_organisation_by_station, name='get-organisation'),
  path('station/organisation/working_society/', views.get_working_society_by_organisation, name='get-working_society'),
] 