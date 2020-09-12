from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count, Q, F
from .models import User, Listing, Bid, Comment, Category


'''
GET view and entry point of website. This view provides all the listings or can also provide listings filtered by category, depending on the get params
'''
def index(request):
    category_id = request.GET.get('category_id', '')
    if category_id:
        category = Category.objects.get(id=category_id)
        listings = category.listing_category\
        .filter(active=True)\
        .all()
        listings.category = category
    else:
        listings = Listing.objects\
        .filter(active=True)\
        .all()
        listing.category = None
    status = {}
    status['code'] = request.GET.get('code', '')
    status['msg'] = request.GET.get('msg', '')
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


'''
POST view for creating a new listing. GET view for viewing the create new listing form
TODO: add backend validation.
'''
@login_required(login_url='/login')
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
        listing = Listing(title=title, description=description, category=category, starting_bid=starting_bid, active=True, owner=request.user, image_url=image_url)
        listing.save()

        # redirect
        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all().order_by('value')
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })

'''
GET view to display a listing with details. a status object is also sent to the template for any messages that needs to be displayed
'''
def listing(request, listing_id):
    if request.method == "POST":
        pass
    else:
        status = {}
        status['code'] = request.GET.get('code', '')
        status['msg'] = request.GET.get('msg', '')
        listing = Listing.objects.get(id=listing_id)
        if not listing.bids.exists():
            listing.price = None
        else:
            listing.price = listing.bids.order_by('-value').all()[0].value
        if request.user.is_authenticated:
            listing.watchlist = request.user.watchListings.filter(id=listing_id).exists()
        else:
            listing.watchlist = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "status": status,
        })


'''
POST view for placing a bid. Bid logic / validation is handled in the backend and status message / code is sent back to the 
listing view so that it can be displayed on the listing page.
'''
@login_required(login_url='/login')
def place_bid(request, listing_id):
    if request.method == "POST":
        value = request.POST["bid"]
        listing = Listing.objects.get(id=listing_id);
        if listing.bids.count() == 0:
            if int(value) < listing.starting_bid:
                status = {
                    "code": '400',
                    "msg": 'Your bid is too low!',
                }
            else:
                bid = Bid(value=value, user=request.user)
                bid.save()
                listing.bids.add(bid)
                listing.save()
                status = {
                    "code": '200',
                    "msg": 'Success!',
                }
        elif int(value) <= listing.bids.order_by('-value').all()[0].value:
            status = {
                "code": '400',
                "msg": 'Your bid is too low!',
            }
        else:
            bid = Bid(value=value, user=request.user)
            bid.save()
            listing.bids.add(bid)
            listing.save()
            status = {
                "code": '200',
                "msg": 'Success!',
            }
        return HttpResponseRedirect(reverse("listing" , args=(listing_id, )) + "?code=" + status["code"] + "&msg=" + status["msg"])
    return HttpResponseRedirect(reverse("index"))


'''
POST view for a listing owner to accept a bid. The listing is then changed to inactive and a winner assigned.
... redirects to the index page.
'''
@login_required(login_url='/login')
def accept_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        bid_id = request.POST['bid_id']
        listing.winner = Bid.objects.get(id=bid_id).user
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))


'''
POST view to add or remove a listing to a user's watchlist.
GET view to view a page showing all the listings on the user's watchlist.
'''
@login_required(login_url='/login')
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


'''
GET view that shows a page with all the listings that a user has made bids on.
'''
@login_required(login_url='/login')
def your_bids(request):
    if Bid.objects.filter(user__id=request.user.id).exists():
        listings = Listing.objects.filter(bids__user = request.user.id).all().distinct()
    else:
        listings = None
    return render(request, "auctions/yourbids.html", {
        "yourbids_listings": listings
    })


'''
POST view to add a comment to a listing. Once the listing is made, the page is reloaded and the new comment displayed.
'''
@login_required(login_url='/login')
def comment(request, listing_id):
    if request.method == "POST":
        if request.POST['comment']:
            listing = Listing.objects.filter(id=listing_id).get()
            comment = Comment(user=request.user, text=request.POST['comment'])
            comment.save()
            listing.comments.add(comment)
            listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


