from django.contrib.auth.models import AbstractUser
from django.db import models


'''
user_id | number of listings (int) | number of listings on watchlist (int) | number of listings with bids on them? (int)
'''

class User(AbstractUser):
	# name = models.CharField(max_length=256)
	pass
	#listings = models.ManyToManyField(Listing, related_name="user_listings")
	# watchlist = models.ManyToManyField(Listing, related_name="user_watchlist")


'''
	A listing can only have one user. It can have many comments and many bids
	listing_id | date | title (string) | description (string) | long_description (string) | category (string) | pic url | starting_bid (number / real) | status (open / close) | owner_user_id
	todo: validators=[MinValueValidator(Decimal('0.01'))]
'''



	# status?
	# pass

class Listing(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField()
	starting_bid =  models.DecimalField(max_digits=6, decimal_places=2)
	category = models.CharField(max_length=64)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	active = models.BooleanField()
	# bids = models.ManyToManyField(Bid, related_name="bids")
	# comments = models.ManyToManyField(Comment, related_name="comments")
	# pass

'''
A comment is made by a particular user and on a particular listing
comment_id | date | user_id | listing_id
'''
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	# pass

'''
Bids are linked to a particular listing and a particular user
bid_id | date | amount (number / real) | user_id (fk) | listing_id (fk) | status
TODO validators=[MinValueValidator(Decimal('0.01'))]
'''
class Bid(models.Model):
	value = models.DecimalField(max_digits=6, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

# first = models.CharField(max_length=64)
#     last = models.CharField(max_length=64)
#     flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

#     origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
#     destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
#     duration = models.IntegerField()





'''
Q: 
Many to many:
- listings and bidding users
- listings and watchlist users -> listing_id | user_id
'''