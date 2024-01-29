from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.WorkingSocietyView.as_view(), name='working_society-view'),
  path('<int:pk>/members/', views.working_society_members, name='working_society-members'),
  path('members/change_society', views.change_members_working_society, name='change-members-society'),
  path('<int:pk>/members/add/', views.WorkingSocietyMembersAddView.as_view(), name='working_society-members-add'),
  path('<int:pk>/members/<int:id>/remove/', views.working_society_members_remove, name='working_society-members-remove'),
  path('create/', views.WorkingSocietyCreateView.as_view(), name='working_society-create'),
  path('<int:pk>/update/', views.WorkingSocietyUpdateView.as_view(), name='working_society-update'),
  path('<int:pk>/delete/', views.delete_working_society, name='working_society-delete'),
]