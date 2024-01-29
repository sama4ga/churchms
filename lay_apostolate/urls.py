from django.urls import path
from . import views

urlpatterns = [
  path('', views.LayApostolateView.as_view(), name='lay_apostolate-view'),
  path('create/', views.LayApostolateCreateView.as_view(), name='lay_apostolate-create'),
  path('<int:pk>/update/', views.LayApostolateUpdateView.as_view(), name='lay_apostolate-update'),
  path('<int:pk>/delete/', views.delete_lay_apostolate, name='lay_apostolate-delete'),
  path('<int:pk>/members/', views.lay_apostolate_members, name='lay_apostolate-members'),
  path('<int:pk>/members/add/', views.LayApostolateMembersAddView.as_view(), name='lay_apostolate-members-add'),
  path('<int:pk>/members/<int:id>/remove/', views.lay_apostolate_members_remove, name='lay_apostolate-members-remove'),
  path('members/update_status/', views.lay_apostolate_members_update_status, name='lay_apostolate-members-update-status'),
] 