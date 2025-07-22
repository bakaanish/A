from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('photobooth/', views.photobooth, name='photobooth'),
    path('tulips/', views.tulips, name='tulips'),
    path('games/', views.games, name='games'),
    path('games/memory/', views.memory_game, name='memory_game'),
    path('games/quiz/', views.quiz_game, name='quiz_game'),
    path('study/', views.study_companion, name='study_companion'),
    path('notes/', views.notes, name='notes'),
    path('flashcards/', views.flashcards, name='flashcards'),
    path('clinical-skills/', views.clinical_skills, name='clinical_skills'),
    path('nclex-prep/', views.nclex_prep, name='nclex_prep'),
    path('nursing-curriculum/', views.nursing_curriculum, name='nursing_curriculum'),
]