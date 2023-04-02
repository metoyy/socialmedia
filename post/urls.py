from django.urls import path, include

from comments.views import CommentAddView
from post import views
from rest_framework.routers import DefaultRouter
from post.views import FavoriteAddOrDeletePost
from like.views import *


router = DefaultRouter()
router.register('', views.PostViewSet)


urlpatterns = [
    path('<int:pk>/comments/', views.PostCommentsView.as_view()),
    path('<int:pk>/comments/add/', CommentAddView.as_view()),
    path('<int:pk>/add_to_fav/', FavoriteAddOrDeletePost.as_view()),
    path('<int:pk>/like/', LikeCreateView.as_view()),
    path('<int:pk>/rmlike/', LikeDeleteView.as_view()),
    path('', include(router.urls)),
]

