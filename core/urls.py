from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  #maps root URL to home view
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('upcoming/<int:project_id>/', views.upcoming_project_detail, name='upcoming_project_detail'),
    path('about/', views.about, name='about'),
    path('team/<int:member_id>/', views.team_member_detail, name='team_member_detail'),
    path('actualites/', views.actualites, name='actualites'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact_view, name='contact'),
]