from django.urls import path, include

from post import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/comments/', views.PostCommentsView.as_view()),
]

