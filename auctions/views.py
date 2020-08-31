from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session


from .models import User, Listing, Bidding, Watchlist

from .forms import ListingForm, BiddingForm

def index(request):
    try:
        listing = Listing.objects.all()
    except listing.DoesNotExist:
        "No Listings Yet"
    context = {
        'object': listing
    }
    return render(request, "auctions/index.html", context)

def createlisting(request):
    creator = Listing.objects.all()
    form = ListingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.lister = request.user
            fs.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create.html", {
            'form': form,
            'creator': creator
        })

def listingpage(request,id):
    try:
        bidform = BiddingForm(request.POST or None)
        listing = Listing.objects.get(id=id)
    except:
        return redirect('index')
    if request.user.username:
        try:
            if Watchlist.objects.get(watcher=request.user.username, listingid=id):
                added=True
        except:
            added = False
    else: 
        added=False
    return render(request, "auctions/listing.html", {
        'object': listing,
        'added': added,
        'bidform': bidform
    })

def addwatch(request, id):
    if request.user.username:
        watchers = Watchlist(watcher = request.user.username, listingid = id)
        watchers.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('index')

def removewatch(request,id):
    if request.user.username:
        try:
            watchers = Watchlist.objects.get(watcher=request.user.username,listingid=id)
            watchers.delete()
            return redirect('listingpage', id=id)
        except:
            return redirect('listingpage', id=id)
    else:
        return redirect('index')

def addbid(request, id):
    bidform = BiddingForm(request.POST or None)
    if request.user.username:
        if request.method == "POST":
            if bidform.is_valid():
                fs = bidform.save(commit=False)
                fs.bidder = request.user
                fs.listingid = id
                fs.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
def watchlist(request):
    return render(request,'auctions/watchlist.html')

def category(request):
    return render(request, "auctions/categories.html")
        

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
