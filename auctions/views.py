from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count, Q, F
from .models import User, Listing, Bid, Comment, Category


def index(request):
    category_id = request.GET.get('category_id', '')
    if category_id:
        category = Category.objects.get(id=category_id)
        listings = category.listing_category\
        .filter(active=True)\
        .annotate(bid=Max("listing__value"))\
        .all()
        listings.category = category
    else:
        listings = Listing.objects\
        .annotate(bid=Max("listing__value"))\
        .filter(active=True)\
        .all()
        listing.category = None
    status = {}
    status['code'] = request.GET.get('code', '')
    status['msg'] = request.GET.get('msg', '')
    print(status)
    # print(request.GET.get('msg', ''))
    categories = Category.objects.all().order_by('value')

    return render(request, "auctions/index.html", {
        "active_listings": listings,
        "categories": categories,
        "status": status
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
        category = Category.objects.get(id=category_id)
        # save to db
        listing = Listing(title=title, description=description, category=category, starting_bid=starting_bid, active=True, user=request.user)
        listing.save()

        # redirect
        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all().order_by('value')
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })


def listing(request, listing_id=''):
    if request.method == "POST":
        pass
    else:
        status = {}
        status['code'] = request.GET.get('code', '')
        status['msg'] = request.GET.get('msg', '')
        print(status)
        listing = Listing.objects\
        .annotate(bid=Max("listing__value"))\
        .annotate(num_bids=Count("listing__id"))\
        .get(id=listing_id);
        # onWatchlist = request.user.watchlist_users.filter(id=listing_id).exists()
        listing.watchlist = listing.users.filter(id=request.user.id).exists()
        listing.comments = Comment.objects.filter(listing__id=listing_id).order_by('-created_at').all()

        if Bid.objects.filter(listing__id=listing_id).exists():
            bids = Bid.objects.filter(listing__id=listing_id).order_by('-value').all()
        else:
            bids = None
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bids": bids,
            "status": status,
        })


@login_required(login_url='/login_view')
def place_bid(request, listing_id):
    print(listing_id)
    if request.method == "POST":
        value = request.POST["bid"]
        # TODO: validate
        listing = Listing.objects.annotate(bid=Max("listing__value")).get(id=listing_id);
        if not listing.bid:
            if int(value) < listing.starting_bid:
                status = {
                    "code": '400',
                    "msg": 'Your bid is too low!',
                }
            else:
                bid = Bid(value=value, user=request.user, listing=listing)
                bid.save() 
                status = {
                    "code": '200',
                    "msg": 'Success!',
                }
        elif int(value) <= listing.bid:
            status = {
                "code": '400',
                "msg": 'Your bid is too low!',
            }
        else:
            bid = Bid(value=value, user=request.user, listing=listing)
            bid.save() 
            status = {
                "code": '200',
                "msg": 'Success!',
            }
        return HttpResponseRedirect(reverse("listing" , args=(listing_id, )) + "?code=" + status["code"] + "&msg=" + status["msg"])
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login_view')
def accept_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bid_id = request.POST['bid_id']
        listing.winner = Bid.objects.get(id=bid_id).user
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
        watchlist_listings = Listing.objects.filter(users__id=request.user.id).annotate(bid=Max("listing__value")).all()
        return render(request, "auctions/watchlist.html", {
            "watchlist_listings": watchlist_listings
        })

@login_required(login_url='/login_view')
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        comment = Comment(user=request.user, listing=listing, text=request.POST['comment'])
        comment.save()
        # listing.comments.add(comment)
        # listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


