from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PostsLikes


@login_required
def post_add_like(request):
    """Добавляем like к посту"""
    if request.is_ajax():

        user_inst = request.user
        post_inst = int(request.POST.get('post_id'))

        post_like = PostsLikes.objects.filter(
            post_id=post_inst,
            liked_by=user_inst,
        ).exists()

        if not post_like:
            PostsLikes.objects.create(
                post_id=post_inst,
                liked_by=user_inst,
            )
        return JsonResponse({
            'added': True,
        })


@login_required
def post_remove_like(request):
    """Удаляем like у поста"""
    if request.is_ajax():
        post_likes_id = int(request.POST.get('post_likes_id'))
        data = {
            'removed': True,
        }
        post_like = PostsLikes.objects.get(id=post_likes_id)
        if request.user:
            post_like.delete()
        return JsonResponse(data)
