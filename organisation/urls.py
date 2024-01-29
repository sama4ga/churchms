from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.OrganisationView.as_view(), name='organisation-view'),
  path('<int:pk>/', views.OrganisationDetailView.as_view(), name='organisation-detail'),
  path('create/', views.OrganisationCreateView.as_view(), name='organisation-create'),
  path('<int:pk>/update/', views.OrganisationUpdateView.as_view(), name='organisation-update'),
  path('<int:pk>/delete/', views.delete_organisation, name='organisation-delete'),
  path('<int:pk>/remove/', views.remove_organisation, name='organisation-remove'),
  path('<int:pk>/info/', views.OrganisationInfoView.as_view(), name='organisation-info'),
  path('<int:id>/info/<int:pk>/update', views.OrganisationInfoUpdateView.as_view(), name='organisation-info-update'),
  path('<int:pk>/members/', views.organisation_members, name='organisation-members'),
  path('members/change_organisation', views.change_members_organisation, name='change-members-organisation'),
  path('search/', views.search_parishioner, name='organisation-members-search'),
  path('station/get_organisation/', views.get_organisation_by_station, name='organisation-get-organisation'),
]