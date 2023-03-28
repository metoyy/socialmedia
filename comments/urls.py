from django.urls import path

from comments import views

urlpatterns = [
    path('', views.CommentCreateView.as_view()),
    path('<int:pk>/', views.CommentDetailView.as_view()),
]
