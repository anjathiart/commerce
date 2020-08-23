from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count, Q
from .models import User, Listing, Bid, Comment, Category


def index(request):
    categories = Category.objects.all().order_by('value')
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active = True),
        "categories": categories
    })

def filter(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    active_category = category.value
    listings = category.listings

    return render(request, "auctions/index.html", {
        "active_listings": listings,
        "categories": categories,
        "active_category": active_category
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login_view')
def create_new(request):
    if request.method == "POST":

        # extract post fields
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category_id = request.POST["category"]

        # save to db
        listing = Listing(title=title, description=description, starting_bid=starting_bid, active=True, owner=request.user)
        listing.save()

        category = Category.objects.get(id=category_id)
        category.listings.add(listing)
        category.save()

        # redirect
        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all().order_by('value')
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })


def listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).get();
    listing.num_bids = listing.bids.count()

    comments = []
    if listing.num_bids > 0:
        listing.min_bid = listing.max_bid.value + 1
        listing.max_bid = listing.bids.order_by('value')[0]
    if listing.comments.count() > 0:
        comments = listing.comments.all()

    # can probably do this via an annotation?
    watchlist = False
    if Listing.objects.filter(id=listing_id).filter(users__id=request.user.id):
        watchlist = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
    })

@login_required(login_url='/login_view')
def place_bid(request, listing_id):
    if request.method == "POST":
        value = request.POST["bid"]
        # TODO: validate
        bid = Bid(value=value, owner=request.user)
        bid.save()
        listing = Listing.objects.get(id=listing_id);
        listing.bids.add(bid)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login_view')
def accept_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bid_id = request.POST['bid_id']
        listing.winner = Bid.objects.get(id=bid_id).owner
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login_view')
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        action = request.POST['toggle']
        listing = Listing.objects.get(id=listing_id)
        if action == "add":
            listing.users.add(request.user)
        if action == "remove":
            listing.users.remove(request.user)
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    else:
        watchlist_listings = Listing.objects.filter(users__id=request.user.id).all()
        return render(request, "auctions/watchlist.html", {
            "watchlist_listings": watchlist_listings
        })


@login_required(login_url='/login_view')
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        comment = Comment(user=request.user,  text=request.POST['comment'])
        comment.save()
        listing.comments.add(comment)
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


