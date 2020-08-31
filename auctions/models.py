from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

CATEGORY = (
    ('FASHION', 'Fashion'), 
    ('TOYS', 'Toys'),
    ('ELECTRONICS', 'Electronics'), 
    ('HOME', 'Home'), 
    ('BEAUTY & HEALTH', 'Beauty & Health'), 
    ('SPORTS', 'Sports'),
    ('PETS', 'Pets'), 
    ('BABY', 'Baby'), 
    ('GROCERY','Grocery'), 
    ('ENTERTAINMENT','Entertainment'),
    )

class User(AbstractUser):
    pass

class Listing(models.Model): 
    productnames = models.CharField(max_length=50)
    descriptions = models.TextField()
    startingbids = models.DecimalField(max_digits=15, decimal_places=2)
    images = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, blank=True, null=True)
    lister = models.CharField(max_length=50, blank=True, null=True)
   #created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productnames

class Bidding(models.Model):
    bidder = models.CharField(max_length=50)
    bidprice = models.DecimalField(max_digits=15, decimal_places=2)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

class Watchlist(models.Model):
    watcher = models.CharField(max_length=50, blank=True, null=True)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

#class Comment(models.Model)
   #comment = models.

    