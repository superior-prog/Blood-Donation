from django.urls import path
from .views import *


urlpatterns = [
    path('', event_home_view, name='event-home'),
    path('create-new-event/', create_event_view, name="create-event"),
    path('<str:pk>/', event_detail_view, name='event-detail'),
    path('edit/<str:pk>/', edit_event_view, name='edit-event'),
    path('delete/<str:pk>/', delete_event_view, name='delete-event'),
]
