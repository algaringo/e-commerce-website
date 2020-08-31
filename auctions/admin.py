from django.contrib import admin
from .models import Listing, Bidding, Watchlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "productnames")

class BiddingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bidprice")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("__str__", "watcher")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)