from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from .forms import *
from .util import *


def index(request):
    active_listings = Listing.objects.filter(active=True).order_by('-created')
    for listing in active_listings:
        get_max_bid(listing)
        print(listing.created)
    return render(request, "auctions/index.html", {"active_listings": active_listings})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
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
                    "auctions/login.html",
                    {"message": "Invalid username and/or password."},
                )
        else:
            return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(
                    request,
                    "auctions/register.html",
                    {"message": "Passwords must match."},
                )

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(
                    request,
                    "auctions/register.html",
                    {"message": "Username already taken."},
                )
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/register.html")


def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        bids_len = len(listing.bids.all())
        get_max_bid(listing)

        if request.user.is_authenticated:
            user_watchlist = Watchlist.objects.get(user=request.user)
            in_user_watchlist = listing in user_watchlist.listings.all()
            user_highest_bid = highest_bid(request.user, listing)
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": listing,
                    "bids_len": bids_len,
                    "in_user_watchlist": in_user_watchlist,
                    "user_highest_bid": user_highest_bid,
                    "bid_form": BidForm(),
                    "comment_form": CommentForm(),
                },
            )
        else:
            return render(request, "auctions/listing.html", {"listing": listing})
    return render(request, "auctions/listing.html")


@login_required
def create(request):
    if request.method == "POST":
        create_form = ListingForm(request.POST)
        if create_form.is_valid():
            data = create_form.cleaned_data
            listing = Listing(
                owner=request.user,
                title=data["title"],
                description=data["description"],
                category=data["category"],
                image_url=data["image_url"],
                starting_bid=data["starting_bid"],
            )
            listing.save()
            return HttpResponseRedirect(
                reverse("listing", args=[listing.id]), {"listing": listing}
            )
        else:
            return render(
                request,
                "auctions/create.html",
                {
                    "create_form": create_form,
                    "error": "Invalid: Please check your inputs for errors.",
                },
            )
    return render(request, "auctions/create.html", {"create_form": ListingForm()})


@login_required
def watchlist_view(request):
    watchlist_listings = Watchlist.objects.get(user=request.user).listings.all().order_by('-created')
    for listing in watchlist_listings:
        if listing.bids.all():
            listing.max_bid = max([bid.bid_price for bid in listing.bids.all()])
        else:
            listing.max_bid = listing.starting_bid
    return render(
        request,
        "auctions/watchlist.html",
        {
            "watchlist_listings": watchlist_listings,
        },
    )


@login_required
def add_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        watchlist = Watchlist.objects.get(user=request.user)
        if not listing in watchlist.listings.all():
            watchlist.listings.add(listing)
    return HttpResponseRedirect(
        reverse(
            "listing",
            args=[
                listing_id,
            ],
        )
    )


@login_required
def remove_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        watchlist = Watchlist.objects.get(user=request.user)
        if listing in watchlist.listings.all():
            watchlist.listings.remove(listing)
    return HttpResponseRedirect(
        reverse(
            "listing",
            args=[
                listing_id,
            ],
        )
    )


@login_required
def bid(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        max_bid = get_max_bid(listing)
        if request.method == "POST":
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                data = bid_form.cleaned_data
                bid_price = float(data["bid_price"])
                starting_bid = listing.starting_bid
                if not max_bid and bid_price < starting_bid:
                    messages.error(request, 'Your bid should be at least the starting bid.')
                elif max_bid and bid_price <= max_bid:
                    messages.error(request, 'Your bid should be higher than the current bid.')
                else:
                    bid = Bid(
                        bidder=request.user,
                        listing=listing,
                        bid_price=bid_price,
                    )
                    bid.save()
                    get_max_bid(listing)
                    bid_form = BidForm()

            # get other context
            bids_len = len(listing.bids.all())
            user_watchlist = Watchlist.objects.get(user=request.user)
            in_user_watchlist = listing in user_watchlist.listings.all()
            user_highest_bid = highest_bid(request.user, listing)
        
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids_len": bids_len,
                "in_user_watchlist": in_user_watchlist,
                "user_highest_bid": user_highest_bid,
                "bid_form": bid_form,
                "comment_form": CommentForm(),
            })
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def close_auction(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        if request.user == listing.owner:
            listing.active = False
            listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def comment(request, listing_id):
    try:
       listing = Listing.objects.get(pk=listing_id)
    except:
        pass
    else:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                data = comment_form.cleaned_data
                text = data["text"]
                comment = Comment(
                    user=request.user,
                    listing=listing,
                    text=text,
                )
                comment.save()
            return render(
                request,
                "auctions/listing.html",
                {"listing": listing, "bid_form": BidForm(), "comment_form": CommentForm()},
            )
    return HttpResponseRedirect(reverse("listing", args=[listing_id,]))


def categories(request):
    categories = [category for category in Listing.CATEGORIES_CHOICES]
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": categories,
        },
    )


def category(request, category):
    active_listings = Listing.objects.filter(active=True).order_by('-created')
    category_listings = []
    for listing in active_listings:
        if listing.category == category:
            category_listings.append(listing)
            get_max_bid(listing)
    for category_tuple in Listing.CATEGORIES_CHOICES:
        if category_tuple[0] == category:
            category_name = category_tuple[1]
            return render(
                request,
                "auctions/category.html",
                {
                    "category_name": category_name,
                    "category_listings": category_listings,
                },
            )
    raise Http404("Category Not Found")
