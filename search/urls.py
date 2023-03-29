from django.urls import path

from search import views

urlpatterns = [
    path('posts/', views.PostSearchView.as_view()),
    path('users/', views.UserSearchView.as_view()),
]
