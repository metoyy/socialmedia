from django.urls import path
from .views import *


urlpatterns = [
    path('', FeedView.as_view()),
]
