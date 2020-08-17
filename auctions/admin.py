from django.contrib import admin

# Register your models here.
from .models import Listing

# Register your models here.

# class ListingAdmin(admin.ModelAdmin):
#     list_display = ("__str__", "duration")

# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    

# admin.site.register(Airport)
admin.site.register(Listing)
# admin.site.register(Passenger, PassengerAdmin)
