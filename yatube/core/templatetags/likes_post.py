from django import template
from django.shortcuts import get_object_or_404
from likes.models import PostsLikes
from posts.models import Post

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, post_id):
    request = context['request']
    return PostsLikes.objects.filter(
        post__id=post_id,
        liked_by=request.user.id,
    ).exists()


@register.simple_tag()
def count_likes(post_id):
    post = get_object_or_404(Post, id=post_id)
    return post.likes.count()


@register.simple_tag(takes_context=True)
def post_likes_id(context, post_id):
    request = context['request']
    return PostsLikes.objects.get(
        post__id=post_id,
        liked_by=request.user.id,
    ).id
