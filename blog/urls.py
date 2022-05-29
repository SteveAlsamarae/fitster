from django.urls import path

from .views import (
    post_list_view,
    post_detail_view,
    user_posts_view,
    add_post_view,
    update_post_view,
    delete_post_view,
    posts_search_view,
    posts_by_tag_view,
)

app_name = "blog"

urlpatterns = [
    path("", post_list_view, name="post_list"),
    path("<str:slug>/", post_detail_view, name="post_detail"),
    path("posts/search", posts_search_view, name="search"),
    path("posts/<str:tag>", posts_by_tag_view, name="posts_by_tag"),
    path("<str:username>/posts", user_posts_view, name="user_posts"),
    path("post/add/", add_post_view, name="add_post"),
    path("post/update/<str:post_id>/", update_post_view, name="update_post"),
    path("post/delete/<str:post_id>/", delete_post_view, name="delete_post"),
]
