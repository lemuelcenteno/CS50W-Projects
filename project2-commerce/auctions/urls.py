from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/add", views.add_watchlist, name="add-watchlist"),
    path(
        "listing/<int:listing_id>/remove",
        views.remove_watchlist,
        name="remove-watchlist",
    ),
    path("listing/<int:listing_id>/close", views.close_auction, name="close-auction"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>/", views.category, name="category"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
