from django.urls import path

from .views import (AddComment, FollowAndUnfollowProfile, FollowIndex,
                    GroupPosts, Index, PostCreate, PostDelete, PostDetail,
                    PostEdit, Profile, Subscribers, Subscriptions)

app_name = 'posts'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('group/<slug>/', GroupPosts.as_view(), name='group_list'),
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path(
        'posts/<int:post_id>/comment/',
        AddComment.as_view(),
        name='add_comment',
    ),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:post_id>/edit/',
         PostEdit.as_view(), name='post_edit'),
    path('posts/<int:post_id>/delete/',
         PostDelete.as_view(), name='post_delete'),
    path('follow/', FollowIndex.as_view(), name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        FollowAndUnfollowProfile.as_view(),
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        FollowAndUnfollowProfile.as_view(),
        name='profile_unfollow'
    ),
    path(
        'profile/<str:username>/subscribers/',
        Subscribers.as_view(),
        name='subscribers'
    ),
    path(
        'profile/<str:username>/subscriptions/',
        Subscriptions.as_view(),
        name='subscriptions'
    ),
]
