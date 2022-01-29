

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('posts', views.PostList.as_view()),
    path('posts/<int:id>/vote', views.CreateVote.as_view()),
    path('posts/<int:id>/', views.PostDetails),

]
