from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from favorite.serializers import FavoriteListSerializer

User = get_user_model()


class FavoriteListView(APIView):

    def get(self, request):
        favs = request.user.favorite_posts.all()
        serializer = FavoriteListSerializer(instance=favs, many=True, context=request.user).data
        serializer = [x for x in serializer]
        return Response(serializer, status=200)

