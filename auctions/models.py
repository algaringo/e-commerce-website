from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils.timezone import now

# CATEGORY = (
#     ('fashion', 'fashion'), 
#     ('toys', 'toys'),
#     ('electronics', 'electronics'), 
#     ('home', 'home'), 
#     ('sports', 'sports'),
#     ('pets', 'pets'), 
#     ('baby', 'baby'), 
#     ('grocery','grocery'), 
#     ('entertainment','entertainment'),
#     )

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Listing(models.Model): 
    productnames = models.CharField(max_length=20)
    descriptions = models.TextField(max_length=500)
    startingbids = models.DecimalField(max_digits=15, decimal_places=2)
    images = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True, default="")
    lister = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.productnames

class Bidding(models.Model):
    bidder = models.CharField(max_length=50, blank=True, null=True)
    bidprice = models.DecimalField(max_digits=15, decimal_places=2)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

class Watchlist(models.Model):
    productnames = models.CharField(max_length=20)
    images = models.URLField(blank=True, null=True)
    finalbid = models.DecimalField(max_digits=15, decimal_places=2)
    lister = models.CharField(max_length=50, blank=True, null=True)
    watcher = models.CharField(max_length=50, blank=True, null=True)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

class Closebid(models.Model):
    productnames = models.CharField(max_length=20)
    images = models.URLField(blank=True, null=True)
    lister = models.CharField(max_length=64, blank=True, null=True)
    bidder = models.CharField(max_length=64, blank=True, null=True)
    listingid = models.IntegerField()
    category = models.CharField(max_length=50, blank=True, null=True)
    finalbid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.listingid}"

class Comment(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(default=now, editable=False)
    comment = models.CharField(max_length=30)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"

    