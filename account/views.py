import uuid

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers
from account.models import CustomUser
from account.sendmail import *

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
    def put(self, request):
        try:
            serializer = serializers.PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except User.DoesNotExist:
            return Response({'msg': 'Code expired or invalid!'}, status=400)
        return Response({'msg': 'Successfully changed password!'}, status=200)
