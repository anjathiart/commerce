from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	def __str__(self):
		return self.username

'''
A model for all possible categories that a user can assign a listing to
'''
class Category(models.Model):
	value = models.CharField(max_length=128)
	def __str__(self):
		return self.value


'''
A bid is made by a user and has a value and data associated with it
'''
class Bid(models.Model):
	value = models.DecimalField(max_digits=12, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	class Meta:
		ordering= ["-value"]


'''
A comment is made by a particular user
'''
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.text

	class Meta:
		ordering= ["-created_at"]

'''
A listing has a title, description, image link, a starting bid (initial price set by owner). It can be active or inactive.
A listing can have many bids and comments associated with it. A listing can belong to a category. Once a bid is accepted, a listing also has a winner
'''
class Listing(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True)
	starting_bid =  models.DecimalField(max_digits=10, decimal_places=2)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	users = models.ManyToManyField(User, blank=True, related_name="watchListings")
	active = models.BooleanField(default=True)
	winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="listingsWon")
	image_url = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name="listing_category")
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	bids = models.ManyToManyField(Bid, blank=True, related_name="bidListings")
	comments = models.ManyToManyField(Comment, blank=True, related_name="listing")
	
	def __str__(self):
		return self.title



