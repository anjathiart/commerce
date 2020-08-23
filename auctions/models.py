from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass


'''
Bids are linked to a particular listing and a particular user
bid_id | date | amount (number / real) | user_id (fk) | listing_id (fk) | status
TODO validators=[MinValueValidator(Decimal('0.01'))]
'''
class Bid(models.Model):
	value = models.DecimalField(max_digits=6, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

'''
A comment is made by a particular user and on a particular listing
comment_id | date | user_id | listing_id
'''
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True)


'''
A listing has a title, description, a starting bid (initial price set by owner). It can be active or inactive.
A listing cas have many bids and comments  associated with it. A listing can belong to a category, but that is kept track of
in the Category model
'''
class Listing(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True)
	starting_bid =  models.DecimalField(max_digits=6, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
	active = models.BooleanField()
	winner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="winner")
	bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
	comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
	# TODO: can put the watchlist users here easily... It is silly to go through a Watchlist model because a specific listing 
	# ... can only be on a specific user's watchlist once.
	users = models.ManyToManyField(User, blank=True, related_name="watchlist_users")


'''
A category has a value and can have many listings associated with it
'''
class Category(models.Model):
	value = models.CharField(max_length=128)
	listings = models.ManyToManyField(Listing, blank=True, related_name="listings_in_category")
