from django.urls import path
from . import views

urlpatterns = [
  path('', views.BaptismView.as_view(), name='baptism-view'),
  path('create/', views.BaptismCreateView.as_view(), name='baptism-create'),
  path('<int:pk>/update/', views.BaptismUpdateView.as_view(), name='baptism-update'),
  path('<int:pk>/', views.BaptismDetailView.as_view(), name='baptism-detail'),
  path('<int:pk>/delete/', views.delete_record, name='baptism-delete'),
]