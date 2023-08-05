from django.urls import path
from message.views import Home, PostDetail, AddPost, UpdatePost, DeletePost, Like, AddComment

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<int:pk>', PostDetail.as_view(), name='detail-post'),
    path('add_post/ ', AddPost.as_view(), name='add-post'),
    path('post/edit/<int:pk>', UpdatePost.as_view(), name='update-post'),
    path('post/<int:pk>/delete', DeletePost.as_view(), name='delete-post'),
    path('like/<int:pk>', Like, name='like-post'),
    path('post/<int:pk>/add_comment/ ', AddComment.as_view(), name='add-comment'),
]
