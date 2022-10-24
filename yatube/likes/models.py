from django.db import models
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostsLikes(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='likes',
    )
    liked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Поставил лайк',
        related_name='like_by',
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liked_by}: {self.post}'

    class Meta:
        verbose_name = 'Post Like'
        verbose_name_plural = 'Post Likes'
