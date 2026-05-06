from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('', views.org_chart, name = 'org'), 
    path('department/<int:pk>/', views.department_detail, name = 'department'),
    path('team-types/', views.team_type_view, name = 'team_types'),
]