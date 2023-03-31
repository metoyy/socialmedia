from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url

from django.urls import path

from . import views


urlpatterns = [
    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('dialogs/create/<int:user_id>/', views.CreateDialogView.as_view(),
         name='create_dialog'),
    path('dialogs/<int:chat_id>/', views.MessagesView.as_view(), name='messages'),
]
