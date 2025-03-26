from django.urls import path
from . import views

urlpatterns = [
    path('', views.myfirst, name='main'),
    path('survey/', views.survey, name='survey'),
    path('testing/', views.testing, name='testing'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('quiz_forms/<int:quiz_id>/', views.form_view, name='quiz_forms'),
    path('score-history/', views.score_history, name='score_history'),
    path('score-history/<int:quiz_id>/', views.score_history_by_id, name='score_history_by_id')
]
