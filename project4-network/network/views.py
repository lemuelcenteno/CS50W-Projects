import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Post, User
from .forms import PostForm


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Show 10 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            post = Post(user=request.user, text=text)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "network/index.html", {"form": form, "page_obj": page_obj}
            )
    return render(
        request, "network/index.html", {"form": PostForm(), "page_obj": page_obj}
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        raise Http404("Username not found.")

    profile_posts = Post.objects.filter(user=profile_user).all().order_by("-timestamp")
    paginator = Paginator(profile_posts, 10)  # Show 10 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "network/profile.html",
        {
            "profile_user": profile_user,
            "page_obj": page_obj,
        },
    )


@login_required
def profile_follow(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        return JsonResponse({"error": "Username not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(
            {
                "user": profile_user.username,
                "followers": profile_user.followers.all().count(),
                "following": profile_user.following.all().count(),
            }
        )

    elif request.method == "PUT":
        data = json.loads(request.body)
        # for updating followers
        if data.get("follow") is not None:
            if data["follow"] and request.user not in profile_user.followers.all():
                profile_user.followers.add(request.user)
            if not data["follow"] and request.user in profile_user.followers.all():
                profile_user.followers.remove(request.user)
            profile_user.save()
            return HttpResponse(status=204)

    # Request for following profile must be PUT or GET
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)


@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post contents or like status
    elif request.method == "PUT":
        data = json.loads(request.body)
        # for updating post contents - allowed only if the user created the post
        if data.get("text") is not None and request.user == post.user:
            post.text = data["text"]
        # for updating likes
        if data.get("liked") is not None:
            if data["liked"] and request.user not in post.likes.all():
                post.likes.add(request.user)
            if not data["liked"] and request.user in post.likes.all():
                post.likes.remove(request.user)
        post.save()
        return HttpResponse(status=204)

    # Request for a post must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)

@login_required
def following_view(request):
    following = request.user.following.all()
    following_posts = []
    for followed_user in following:
        following_posts.extend( followed_user.posts.all())

    # sort in reverse chronological order
    following_posts = sorted(following_posts, reverse=True, key=lambda post: post.timestamp)

    paginator = Paginator(following_posts, 10)  # Show 10 posts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "network/following.html",
        {
            "page_obj": page_obj,
        },
    )
    