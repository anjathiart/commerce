from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count, Q
from .models import User, Listing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active = True)
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
        category = request.POST["category"]

        # save to db
        listing = Listing(title=title, description=description, starting_bid=starting_bid, category=category, active=True, owner=request.user)
        listing.save()

        # redirect
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html")


def listing(request, listing_id):
    page_data = {}

    listing = Listing.objects.filter(id=listing_id)\
    .annotate(max_bid=Max('bids__value'), num_bids=Count('bids'))\
    .get(); 

    watchlist = False
    if Listing.objects.filter(users__id=request.user.id):
        watchlist = True

    if listing.owner == request.user:
        print('owner')
    else:
        # check if user has this liting on their wishlist
        # wishlist_users = Listing.objects.values_list('wishlist_users', flat=True).filter(id = listing_id).get()
        print('no')
            # print('user has listing in wishlist')


    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.filter(id = listing_id).get(),
        "watchlist": watchlist
    })

@login_required(login_url='/login_view')
def place_bid(request, listing_id):
    print('bid)')
    if request.method == "POST":
        value = request.POST["bid"]
        # TODO: validate
        bid = Bid(value=value, owner=request.user)
        bid.save()
        listing = Listing.objects.get(id=listing_id);
        listing.bids.add(bid)
        listing.save();
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login_view')
def watchlist(request):
    print('watchlist')
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        action = request.POST['toggle']
        listing = Listing.objects.get(id=listing_id)
        if action == "add":
            listing.users.add(request.user)
            listing.save()
        if action == "remove":
            listing.users.remove(request.user)
            listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    else:
        watchlist_listings = Listing.objects.filter(users__id=request.user.id)
        return render(request, "auctions/watchlist.html", {
            "watchlist_listings": watchlist_listings
        })



