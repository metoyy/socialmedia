from django.urls import path, include

from post import views
from rest_framework.routers import DefaultRouter
from post.views import FavoriteAddOrDeletePost

router = DefaultRouter()
router.register('', views.PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/comments/', views.PostCommentsView.as_view()),
    path('<int:pk>/add_to_fav/', FavoriteAddOrDeletePost.as_view()),

]

