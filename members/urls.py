from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('survey/', views.survey, name='survey'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('myfirst/', views.myfirst, name='testing'),
]
