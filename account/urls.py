from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from favorite.views import FavoriteListView
from . import views


urlpatterns = [
    path('', views.UserListApiView.as_view()),              # GET list of accounts (requires Authentication)
    path('<int:pk>/', views.DetailUser.as_view()),          # GET returns detailed view of account
                                                            # (requires authentication)
    path('register/', views.RegistrationView.as_view()),    # POST registration, takes (email, first_name,
                                                            # last_name, username, password, password2)
    path('activate/', views.ActivationView.as_view()),      # POST takes (code)
    path('login/', views.LoginView.as_view()),              # POST login into account. takes (email, password)
    path('refresh/', TokenRefreshView.as_view()),           # POST refreshes JWT token, takes (refresh=token)
    path('reset/', views.PasswordResetView.as_view()),      # POST takes (email), if exists, sends email with code
                                                            # PUT takes (password_reset_code=code, password, password2)
                                                            # and changes user password with new given
    path('friends/',                               # GET (requires Auth) returns Friends by id of user
         views.FriendListView.as_view()),
    path('friends/<int:pk>/', views.FriendDeleteView.as_view()),

    path('<int:pk>/send_friend_request/',
         views.SendFriendRequestView.as_view(),
         name='send friend request'),
    path('friend_requests/',
         views.FriendRequestsListView.as_view()),
    path('friend_requests/<int:pk>/',
         views.HandleFriendRequestView.as_view(),
         name='accept friend request'),
    path('favorites/', FavoriteListView.as_view()),
    path('balance/', views.BalanceView.as_view()),
    path('balance/topup/', views.TopUpBalanceView.as_view()),

]

