from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='church-home'),
    path('calendar/event/', views.EventListView.as_view(), name='calendar-event-view'),
    path('calendar/event/create/', views.EventCreateView.as_view(), name='calendar-event-create'),
    path('calendar/event/<int:pk>/', views.EventDetailView.as_view(), name='calendar-event-detail'),
    path('calendar/event/<int:pk>/update/', views.EventUpdateView.as_view(), name='calendar-event-update'),
    path('calendar/get_event/', views.get_events, name='calendar-get-events'),
    path('calendar/create_event/', views.create_event, name='calendar-save-events'),
    path('calendar/update_event/<int:pk>/', views.update_event, name='calendar-edit-event'),
    path('calendar/view_event/<int:pk>/', views.view_event, name='calendar-view-event'),
    path('calendar/delete_event/<int:pk>/', views.delete_event, name='calendar-delete-event'),
]