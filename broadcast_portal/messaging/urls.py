from django.urls import path
from . import views


app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name = 'inbox'), 
    path('sent/', views.sent, name = 'sent'), 
    path('drafts/', views.drafts, name = 'drafts'),
    path('<int:pk>/', views.message_detail, name = 'detail'), 
    path('compose/', views.compose, name = 'compose'), 
]