from django.urls import path
from . import views

urlpatterns = [
  path('', views.MatrimonyView.as_view(), name='matrimony-view'),
  path('create/', views.MatrimonyCreateView.as_view(), name='matrimony-create'),
  path('<int:pk>/update/', views.MatrimonyUpdateView.as_view(), name='matrimony-update'),
  path('<int:pk>/', views.MatrimonyDetailView.as_view(), name='matrimony-detail'),
  path('<int:pk>/delete/', views.delete_record, name='matrimony-delete'),
]