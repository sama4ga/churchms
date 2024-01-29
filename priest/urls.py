from django.urls import path
from . import views

urlpatterns = [
  path('', views.PriestView.as_view(), name='priest-view'),
  path('create/', views.PriestCreateView.as_view(), name='priest-create'),
  path('<int:pk>/update/', views.PriestUpdateView.as_view(), name='priest-update'),
  path('<int:pk>/', views.PriestDetailView.as_view(), name='priest-detail'),
  path('<int:pk>/delete/', views.delete_priest, name='priest-delete'),
]