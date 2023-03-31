from django.urls import path
from . import views

urlpatterns = [
    path('userlist_info/', views.UserListView.as_view()),
    path('postlist_info/', views.PostListView.as_view()),
    path('overall_stats/', views.OverallStatsView.as_view()),

]
