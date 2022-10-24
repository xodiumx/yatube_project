from django.urls import path

from . import views

app_name = 'likes'

urlpatterns = [
    path('add/', views.post_add_like, name='add'),
    path('remove/', views.post_remove_like, name='remove'),
]
