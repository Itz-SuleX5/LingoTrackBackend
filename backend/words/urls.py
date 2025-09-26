from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.get_word_for_user, name='get-random-unknown-word'),
    path('mark/', views.mark_user_word, name='mark-user-word'),
    path('my-words/', views.get_user_words_by_status, name='get-user-words-by-status'),
]