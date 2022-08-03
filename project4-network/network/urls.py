from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.profile_follow, name="profile-follow"),
    path("post/<int:post_id>", views.post, name="post"),
    path("following", views.following_view, name="following")
]
