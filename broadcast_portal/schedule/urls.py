from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_list, name='list'),
    path('create/', views.create_meeting, name='create'),
    path('monthly/', views.monthly_view, name='monthly'),
    path('<int:pk>/', views.meeting_detail, name='detail'),
]
