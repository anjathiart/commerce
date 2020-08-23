from django.contrib import admin

# Register your models here.
from .models import Listing, Bid, Category, Comment

# Register your models here.

# class ListingAdmin(admin.ModelAdmin):
#     list_display = ("__str__", "duration")

# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    

admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
