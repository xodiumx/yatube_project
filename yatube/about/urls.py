from django.views.decorators.cache import cache_page
from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path(
        'author/',
        cache_page(900)(views.AboutAuthorView.as_view()),
        name='author',
    ),
    path(
        'tech/',
        cache_page(900)(views.AboutTechView.as_view()),
        name='tech',
    ),
]
