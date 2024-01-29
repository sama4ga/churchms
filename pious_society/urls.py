from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.PiousSocietyView.as_view(), name='pious_society-view'),
  path('create/', views.PiousSocietyCreateView.as_view(), name='pious_society-create'),
  path('<int:pk>/update/', views.PiousSocietyUpdateView.as_view(), name='pious_society-update'),
  path('<int:pk>/delete/', views.delete_pious_society, name='pious_society-delete'),
  path('<int:pk>/members/', views.pious_society_members, name='pious_society-members'),
  path('<int:pk>/members/add/', views.PiousSocietyMembersAddView.as_view(), name='pious_society-members-add'),
  path('<int:pk>/members/<int:id>/remove/', views.pious_society_members_remove, name='pious_society-members-remove'),
  path('members/status/update/', views.pious_society_members_update_status, name='pious_society-members-update-status'),
] 