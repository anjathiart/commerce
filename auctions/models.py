from django.contrib.auth.models import AbstractUser
from django.db import models


'''
user_id | number of listings (int) | number of listings on watchlist (int) | number of listings with bids on them? (int)
'''

class User(AbstractUser):
    pass




'''
A listing can only have one user. It can have many comments and many bids
listing_id | date | title (string) | description (string) | long_description (string) | category (string) | pic url | starting_bid (number / real) | status (open / close) | owner_user_id
'''

class listings():
	pass



'''
Bids are linked to a particular listing and a particular user
bid_id | date | amount (number / real) | user_id (fk) | listing_id (fk) | status
'''
class bids():
	pass


'''
A comment is made by a particular user and on a particular listing
comment_id | date | user_id | listing_id
'''
class comments():
	pass



'''
Q: 
Many to many:
- listings and bidding users
- listings and watchlist users -> listing_id | user_id
'''