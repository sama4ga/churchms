from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.StationView.as_view(), name='station-view'),
  path('create/', views.StationCreateView.as_view(), name='station-create'),
  path('<int:pk>/update/', views.StationUpdateView.as_view(), name='station-update'),
  path('<int:pk>/members/', views.StationMembersView.as_view(), name='station-members'),
  path('<int:pk>/delete/', views.delete_station, name='station-delete'),
  path('<int:pk>/organisations/', views.station_organisations, name='station-organisations'),
  path('members/change_station/', views.change_members_station, name='change-members-station'),
] 