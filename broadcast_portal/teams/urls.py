from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='list'),
    path('<int:pk>/', views.team_detail, name='detail'),
    path('<int:pk>/email/', views.email_team, name='email_team'),
    path('<int:pk>/add-dependency/', views.add_dependency, name='add_dependency'),
    path('dependency-map/', views.dependency_map, name='dependency_map'),
]
