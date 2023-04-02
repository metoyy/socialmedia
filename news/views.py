from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post
from recomendation.models import Recommendation
from recomendation.serializers import *

User = get_user_model()


class FeedView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):

        def get_recommendation(user):
            from random import choice

            try:
                usr = User.objects.get(id=user.id)
                recos = usr.recommend.members.all()
                recos_po = usr.recommend.posts.all()
                recommends = usr.recommend.members
                recommends_po = usr.recommend.posts
                for x in recos:
                    recommends.remove(x)
                for y in recos_po:
                    recommends_po.remove(y)

            except Recommendation.DoesNotExist:
                Recommendation.objects.create(author=request.user)
            members = User.objects.all().order_by('likes')
            posts = Post.objects.all().order_by('likes')
            value = 3 if members.count() >= 3 else members.count()
            value2 = posts.count()
            list_of_posts = []
            list_of_members = []

            def validate_member(qs_members, list_members, user_logged):
                friends = User.objects.get(id=user_logged.id).friends.all()
                memb = choice(qs_members)
                if not memb == user_logged and memb not in list_members and memb not in friends:
                    less = qs_members.exclude(id=memb.id)
                    return memb
                else:
                    less = qs_members.exclude(id=memb.id)
                    return validate_member(less, list_members, user_logged)

            for x in range(value):
                list_of_members.append(validate_member(members, list_of_members, user))
            for y in range(value2):
                list_of_posts.append(validate_member(posts, list_of_posts, user))
            recomm = Recommendation.objects.get(author=user)
            for item in list_of_members:
                recomm.members.add(item)
            for i in list_of_posts:
                recomm.posts.add(i)
            return list_of_members, list_of_posts
        get_recommendation(request.user)
        recommend = Recommendation.objects.get(author=request.user)
        serializer = RecommendationSerializer(instance=recommend)
        return Response(serializer.data, status=200)
