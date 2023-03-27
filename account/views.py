import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers
from account.models import CustomUser, FriendRequest
from account.sendmail import *
from account.permissions import *

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirmation_mail(user.email, user.activation_code)
            except:
                return Response({'msg': 'Registered but could not send email.',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class ActivationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ActivationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Successfully activated!'}, status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = permissions.IsAuthenticated,


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            email = request.data['email']
            assert '@' in email
            user = CustomUser.objects.get(email=email)
            if user.password_reset_code != '':
                return Response({'msg': 'Code already sent, please check your inbox!'}, status=200)
            user.password_reset_code = uuid.uuid4()
            user.save()
        except:
            return Response({'msg': 'Invalid email or not found!'}, status=400)
        send_password_reset(user.email, user.password_reset_code)
        return Response({'msg': 'Confirmation code sent!'}, status=200)

    @staticmethod
    def put(request):
        try:
            serializer = serializers.PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except User.DoesNotExist:
            return Response({'msg': 'Code expired or invalid!'}, status=400)
        return Response({'msg': 'Successfully changed password!'}, status=200)


class DetailUser(APIView):

    permission_classes = permissions.IsAuthenticated,

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = serializers.UserSerializer(instance=user)
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        try:
            if request.user.id != pk:
                return Response({'msg': 'You cant change other user\'s data!'}, status=400)
            user = User.objects.get(id=pk)
            serializer = serializers.UserModifySerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=404)

    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if request.user.id != pk:
                return Response({'msg': 'You cant change other user\'s data!'}, status=400)
            serializer = serializers.UserModifySerializer(instance=user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=404)


@login_required
def send_friend_request(request, pk):
    from_user = request.user
    try:
        to_user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'msg': 'User not found'}, status=404)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return Response({'msg': 'Friend request sent!'}, status=201)
    else:
        return Response({'msg': 'Friend request was already sent!'}, status=200)


@login_required
def handle_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(id=pk)
    except FriendRequest.DoesNotExist:
        return Response({'msg': 'Friend request not found!'}, status=404)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return Response({'msg': 'Friend request accepted!'}, status=200)
    else:
        return Response({'msg': 'Friend request not accepted!'}, status=200)


class FriendListView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request, pk=None):
        user = User.objects.get(id=request.user.id if not pk else pk)
        serializer = serializers.FriendListSerializer(instance=user)
        return Response(serializer.data, status=200)


