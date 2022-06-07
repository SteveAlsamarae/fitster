from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from utils import paginate

from .models import Post
from .forms import AddPostForm


# =====================
# Utils functions    #
# =====================


def get_posts_tags(length: int = 5) -> list:
    """This function returns a list of tags with the given length

    Args:
        length (int): The length of the tags list

    Returns:
        list: The list of tags
    """

    posts = Post.objects.all()
    tags = []
    for post in posts:
        for tag in post.get_comma_separated_tags():
            if tag not in tags:
                tags.append(tag)
    tags = tags[:length]

    return tags


# =================================
# Blog views starts from here     #
# =================================


def post_list_view(request: HttpRequest) -> HttpResponse:
    """This view returns a list of all posts

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    posts = Post.objects.all().order_by("-created_at")
    tags = get_posts_tags(15)

    page_obj = paginate(request, posts, 10)

    return render(
        request, "blog/posts/post_list.html", {"page_obj": page_obj, "tags": tags}
    )


def post_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """This view returns a single post with the given slug

    Args:
        request (HttpRequest): The request object
        slug (str): The slug of the post

    Returns:
        HttpResponse: The response object
    """

    post = get_object_or_404(Post, slug=slug)
    tags = ", ".join(post.get_comma_separated_tags())
    return render(request, "blog/posts/post_detail.html", {"post": post, "tags": tags})


def posts_by_tag_view(request: HttpRequest, tag: str) -> HttpResponse:
    """This view returns a list of all posts with the given tag

    Args:
        request (HttpRequest): The request object
        tag (str): The tag of the posts

    Returns:
        HttpResponse: The response object
    """

    posts = Post.objects.filter(tags__contains=tag).order_by("-created_at")
    tags = get_posts_tags(15)

    page_obj = paginate(request, posts, 10)

    return render(
        request, "blog/posts/post_list.html", {"page_obj": page_obj, "tags": tags}
    )


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """This view returns a list of all posts from the query

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    posts = Post.objects.all().order_by("-created_at")
    tags = get_posts_tags(15)

    if request.htmx:
        query = request.GET.get("q")

        if query:
            posts = Post.objects.filter(title__icontains=query)

        page_obj = paginate(request, posts, 10)
        if posts:
            return render(
                request,
                "_partials/blog/post_rows.html",
                {
                    "posts": posts,
                    "query": query,
                    "tags": tags,
                    "page_obj": page_obj,
                },
            )
        else:
            return render(request, "_partials/blog/no_post.html", {"query": query})
    else:
        page_obj = paginate(request, posts, 10)
        return render(
            request,
            "blog/posts/post_list.html",
            {
                "posts": posts,
                "tags": tags,
                "page_obj": page_obj,
            },
        )


@login_required
def user_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    """This view returns a list of all posts by the given user

    Args:
        request (HttpRequest): The request object
        username (str): The username of the user

    Returns:
        HttpResponse: The response object
    """
    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    page_obj = paginate(request, posts, 10)

    return render(
        request, "blog/posts/user_posts.html", {"posts": posts, "page_obj": page_obj}
    )


@login_required
def add_post_view(request: HttpRequest) -> HttpResponse:
    """This view adds a post

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    form = AddPostForm()

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post added successfully")
            return redirect(reverse("blog:post_detail", args=[post.slug]))

    return render(request, "blog/posts/post_add.html", {"form": form})


@login_required
def update_post_view(request: HttpRequest, post_id: str) -> HttpResponse:
    """This view updates the post with the given id

    Args:
        request (HttpRequest): The request object
        post_id (str): The uuid of the post

    Returns:
        HttpResponse: The response object
    """

    post = get_object_or_404(Post, id=post_id)
    form = AddPostForm(instance=post)

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post updated successfully")
            return redirect(reverse("blog:post_detail", args=[post.slug]))

    return render(request, "blog/posts/post_update.html", {"post": post, "form": form})


@login_required
def delete_post_view(request: HttpRequest, post_id: str) -> HttpResponse:
    """This view deletes the post with the given id

    Args:
        request (HttpRequest): The request object
        post_id (str): The uuid of the post

    Returns:
        HttpResponse: The response object
    """

    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            post.delete()
            messages.success(request, "Post deleted successfully")
            return redirect(reverse("blog:user_posts", args=[request.user.username]))

    return redirect(reverse("blog:post_list"))
