from django.urls import path
from . import views

urlpatterns = [
  path('', views.CommunionView.as_view(), name='communion-view'),
  path('create/', views.CommunionCreateView.as_view(), name='communion-create'),
  path('<int:pk>/update/', views.CommunionUpdateView.as_view(), name='communion-update'),
  path('<int:pk>/', views.CommunionDetailView.as_view(), name='communion-detail'),
  path('<int:pk>/delete/', views.delete_record, name='communion-delete'),
]