from django.urls import path
from . import views

urlpatterns = [
  path('', views.ConfirmationView.as_view(), name='confirmation-view'),
  path('create/', views.ConfirmationCreateView.as_view(), name='confirmation-create'),
  path('<int:pk>/update/', views.ConfirmationUpdateView.as_view(), name='confirmation-update'),
  path('<int:pk>/', views.ConfirmationDetailView.as_view(), name='confirmation-detail'),
  path('<int:pk>/delete/', views.delete_record, name='confirmation-delete'),
]