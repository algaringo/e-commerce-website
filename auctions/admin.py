from django.contrib import admin
from .models import Listing, Bidding, Watchlist, Closebid, Comment, Category

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "productnames")

class BiddingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bidprice")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("__str__", "watcher")

class ClosebidAdmin(admin.ModelAdmin):
    list_display = ("__str__", "lister")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Closebid, ClosebidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)