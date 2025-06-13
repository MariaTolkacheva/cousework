from django.urls import path

from members import views

urlpatterns = [
    path('', views.myfirst, name='main'),
    path('history/', views.history, name='history'),
    path('survey/', views.survey, name='survey'),
    path('materials', views.materials, name='materials'),
    path('askllm', views.askllm_view, name='askllm_view'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('quiz_forms/<int:quiz_id>/', views.form_view, name='quiz_forms'),
    path('score-history/', views.score_history, name='score_history'),
    path('score-history/<int:quiz_id>/', views.score_history_by_id,
         name='score_history_by_id'),
    path("check_compare_results/<int:quiz_id>/", views.check_compare_results,
         name="check_compare_results"),
    path('start_quiz/<int:quiz_id>/', views.start_quiz_processing,
         name='start_quiz')
]
