from django.urls import path
from . import views

urlpatterns = [
    path('albums/', views.album_list, name='album_list'),
    path('album/new/', views.album_create, name='album_create'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),
]
