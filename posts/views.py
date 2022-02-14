
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import CreateUserSerializer, PostSerializer, VoteSerializer
from .models import Post, Vote
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission


def home(request):
    return HttpResponse("hello")


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


# @api_view(['GET'])
# def PostDetails(request, id):
#     post = Post.objects.get(id=id)
#     serializer = PostSerializer(post)
#     return Response(serializer.data)

# building custom permission(object level)

class PostUserPermission(BasePermission):
    message = "Only the author can edit this post"

    def has_object_permission(self, request, view, obj):
        print("obj :", obj)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.poster == request.user


class PostDetails(generics.RetrieveUpdateDestroyAPIView, PostUserPermission):
    def get_object(self):
        return Post.objects.get(id=self.kwargs['id'])

    serializer_class = PostSerializer
    permission_classes = [PostUserPermission]  # custom made permission


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


# creating new user

class CreateNewUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
