from django.contrib.auth import get_user_model
from rest_framework import permissions


User = get_user_model()


class IfPrivateAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.id, view.kwargs['pk'])
        try:
            requested_user = User.objects.get(id=view.kwargs['pk'])
        except User.DoesNotExist:
            return True
        if request.user.id == view.kwargs['pk']:
            return True
        elif request.user.id != view.kwargs['pk'] and requested_user.private_account is True:
            if request.user in requested_user.related_friends.all():
                return True
            else:
                return False
        else:
            return False


class IsReceiverOfRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id == view.request.user.id:
            return True
        return False
