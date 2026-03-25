from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('words/', views.word_list, name='word_list'),
    path('words/<int:pk>/', views.word_detail, name='word_detail'),
    path('words/new/', views.add_word, name='add_word'),
    path('words/<int:pk>/edit/', views.edit_word, name='edit_word'),
    path('words/<int:pk>/delete/', views.delete_word, name='delete_word'),
    path('definition/<int:pk>/vote/', views.vote_definition, name='vote_definition'),
]