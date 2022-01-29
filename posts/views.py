from rest_framework.exceptions import ValidationError
from django.http import HttpResponse, request, response
from rest_framework import generics, permissions

from .serializers import PostSerializer, VoteSerializer


from .models import Post, Vote
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


def home(request):
    return HttpResponse("hello")


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print("helloooo", serializer.validated_data)
        serializer.save(poster=self.request.user)


@api_view(['GET'])
def PostDetails(request, id):
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post)
    print("dhfkhfkj", serializer.data)
    return Response(serializer.data)


class CreateVote(generics.CreateAPIView):

    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['id'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You have already voted for this post :)")
        serializer.save(voter=self.request.user,
                        post=Post.objects.get(id=self.kwargs['id']))
