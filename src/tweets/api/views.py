from rest_framework.generics import ListAPIView, CreateAPIView
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultPagination


class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_q = Tweet.objects.filter(pk=pk)
        message = "Not allowed"
        if tweet_q.exists() and tweet_q.count() == 1:
            new_tweet = Tweet.objects.retweet(request.user, tweet_q.first())
            if new_tweet is not None:
                data = TweetModelSerializer(new_tweet).data
                return Response(data)
            message = "Cannot retweet the same tweet in 1 day "
        return Response({"message": message}, status=400)

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_q = Tweet.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated:
            is_liked = Tweet.objects.like_toggle(request.user, tweet_q.first())
            return Response({'liked': is_liked})
        return Response({"message": message}, status=400)



class TweetCreateAPIView(CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetDetailAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get("pk")
        qs = Tweet.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"parent_id_null": 'parent_id IS NULL'})
        return qs.order_by("-parent_id_null", "timestamp")


class SearchTweetAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all().order_by("-timestamp")
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(SearchTweetAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        q = self.queryset
        query = self.request.GET.get("q", None)
        if query is not None:
            q = q.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return q



class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("username")
        if requested_user:
            q = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
        else:
            users_im_following = self.request.user.profile.get_following()
            q1 = Tweet.objects.filter(user__in=users_im_following)
            q2 = Tweet.objects.filter(user=self.request.user)
            q = (q1 | q2).distinct().order_by("-timestamp")

        query = self.request.GET.get("q", None)
        if query is not None:
            q = q.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return q

#
# class SearchAPIView(generics.ListAPIView):
#         serializer_class = TweetModelSerializer
#         pagination_class = StandardResultPagination
#
#         def get_queryset(self, *args, **kwargs):
#             q = Tweet.objects.order_by("-timestamp")
#             query = self.request.GET.get("q", None)
#             if query is not None:
#                 q = q.filter(
#                     Q(content__icontains=query) |
#                     Q(user__username__icontains=query)
#                 )
#             return q