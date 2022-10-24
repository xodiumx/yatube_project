from django.contrib import admin

from .models import PostsLikes


@admin.register(PostsLikes)
class PostsLikesAdmin(admin.ModelAdmin):
    autocomplete_fields = ('liked_by', 'post')
    list_display = ('pk', 'post', 'liked_by', 'date_created')
