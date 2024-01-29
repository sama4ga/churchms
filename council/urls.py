from django.urls import path
from . import views

urlpatterns = [
  path('', views.CouncilListView.as_view(), name='council-view'),
  path('create/', views.CouncilCreateView.as_view(), name='council-create'),
  path('<int:pk>/update/', views.CouncilUpdateView.as_view(), name='council-update'),
  path('<int:pk>/delete/', views.delete_council, name='council-delete'),
  path('<int:pk>/station/<int:id>/remove', views.remove_station, name='council-remove-station'),
  path('head/create/', views.CouncilHeadCreateView.as_view(), name='council-head-create'),
  path('head/<int:pk>/update/', views.CouncilHeadUpdateView.as_view(), name='council-head-update'),
  path('head/', views.CouncilHeadListView.as_view(), name='council-head-view'),
  path('head/<int:pk>/delete/', views.delete_councilhead, name='council-head-delete'),
  ]