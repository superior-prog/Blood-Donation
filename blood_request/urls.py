from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('create-new-request/', create_request, name="create-request"),
    path('edit-request/<str:pk>/', edit_request_view, name="edit-request"),
    path('delete-request/<str:pk>/', delete_request_view, name="delete-request"),
    path('request/<str:pk>/', request_detail_view, name='request-detail'),
]
