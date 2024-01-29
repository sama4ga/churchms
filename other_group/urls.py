from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.OtherGroupView.as_view(), name='other_group-view'),
  path('create/', views.OtherGroupCreateView.as_view(), name='other_group-create'),
  path('<int:pk>/update/', views.OtherGroupUpdateView.as_view(), name='other_group-update'),
  path('<int:pk>/delete/', views.delete_other_group, name='other_group-delete'),
  path('<int:pk>/members/', views.other_group_members, name='other_group-members'),
  path('<int:pk>/members/add/', views.OtherGroupMembersAddView.as_view(), name='other_group-members-add'),
  path('<int:pk>/members/<int:id>/remove/', views.other_group_members_remove, name='other_group-members-remove'),
  path('members/update_status/', views.other_group_members_update_status, name='other_group-members-update-status'),
] 