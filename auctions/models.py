from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	def __str__(self):
		return self.username

'''
A category has a value and can have many listings associated with it
'''
class Category(models.Model):
	value = models.CharField(max_length=128)

'''
A listing has a title, description, a starting bid (initial price set by owner). It can be active or inactive.
A listing cas have many bids and comments  associated with it. A listing can belong to a category
'''
class Listing(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True)
	starting_bid =  models.DecimalField(max_digits=10, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
	active = models.BooleanField(default=True)
	winner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="winner")
	image_url = models.CharField(max_length=1024, null=True)
	users = models.ManyToManyField(User, blank=True, related_name="watchlist_users")
	category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name="listing_category")

'''
Bids are linked to a particular listing and a particular user
bid_id | date | amount (number / real) | user_id (fk) | listing_id (fk) | status
TODO validators=[MinValueValidator(Decimal('0.01'))]
'''
class Bid(models.Model):
	value = models.DecimalField(max_digits=6, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')

'''
A comment is made by a particular user and on a particular listing
comment_id | date | user_id | listing_id
'''
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

