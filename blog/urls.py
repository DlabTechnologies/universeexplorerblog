
from django.urls import path, include
from blog import views
from .feeds import LatestPostFeed


app_name = 'blog'

urlpatterns = [
    
    path(r'<id>/<slug>/',  views.post_detail, name="post_detail"),
    path(r'post_create/',  views.post_create, name="post_create"),
    path(r'<id>/<slug>/post_edit/',  views.post_edit  , name="post_edit"),
    path(r'<id>/<slug>/post_delete/',  views.post_delete  , name="post_delete"),
    path(r'<id>/<slug>/favourite_post/',  views.favourite_post, name="favourite_post"),
    path(r'favourites/',  views.post_favourite_list, name="post_favourite_list"),
    path(r'feed/', LatestPostFeed(), name='post_feed'),
    
    
    
    
]

