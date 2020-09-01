from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from datetime import datetime


from .models import User, Listing, Bidding, Watchlist, Closebid

from .forms import ListingForm, BiddingForm

def index(request):
    listing = Listing.objects.all()
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount=len(watch)
    except:
        watchcount=None
    return render(request, "auctions/index.html", {
        'object': listing,
        'watchcount': watchcount
    })

@login_required
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
        try:
            listing = Listing.objects.get(id=id)
            if listing.lister == request.user.username :
                lister = True
            else:
                lister = False
        except:
            return redirect('index')
    else: 
        added = False
        lister = False
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        bid = Bidding.objects.filter(listingid=id)
        watchcount = len(watch)
        bidcount = len(bid)
    except:
        watchcount = None
        bicount = None
    return render(request, "auctions/listing.html", {
        'object': listing,
        'added': added,
        'bidform': bidform,
        "watchcount": watchcount,
        "error":request.COOKIES.get('error'),
        "success":request.COOKIES.get('success'),
        "bidcount": bidcount,
        "lister": lister
    })

@login_required
def addwatch(request, id):
    if request.user.username:
        watchers = Watchlist(watcher = request.user.username, listingid = id)
        watchers.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
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

@login_required
def bid(request, listingid):
    current = Listing.objects.get(id=listingid)
    current = current.startingbids
    bidform = BiddingForm(request.POST or None)
    if request.user.username:
        bid = float(request.POST.get("bidprice"))
        if bid > current:
            listing = Listing.objects.get(id=listingid)
            listing.startingbids = bid
            listing.save()
            try:
                if  Bidding.objects.filter(id=listingid):
                    bidrow = Bidding.objects.filter(id=listingid)
                    bidrow.delete()
                fs = bidform.save(commit=False)
                fs.bidder = request.user.username
                fs.listingid = listingid
                fs.save()                                                      
            except:
                fs = bidform.save(commit=False)
                fs.bidder = request.user
                fs.listingid = listingid
                fs.save()   
            response = redirect('listingpage', id=listingid)
            response.set_cookie('success','Successful Bid! Your bid is the current highest bid.', max_age=1)
            return response
        else:
            response = redirect('listingpage', id=listingid)
            response.set_cookie('error','Your bid must be higher than the current price!', max_age=1)
            return response
    else:
        return redirect('index')

@login_required
def watchlist(request):
    try:
        w = Watchlist.objects.filter(watcher=request.user.username)
        items = []
        for i in w:
            items.append(Listing.objects.filter(id=i.id))
        try:
            w = Watchlist.objects.filter(watcher=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,"auctions/watchlist.html",{
            "items":items,
            "wcount":wcount
        })
    except:
        try:
            w = Watchlist.objects.filter(watcher=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,"auctions/watchlist.html",{
            "items":None,
            "wcount":wcount
        })
        
@login_required
def closebid(request, listingid):
    if request.user.username:
        try:
            listing = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        closebid = Closebid()
        name = listing.productnames
        closebid.lister = listing.lister
        closebid.listingid = listingid
        try:
            bid = Bidding.objects.get(listingid=listingid,bidprice=listing.startingbids)
            closebid.bidder = bid.bidder
            closebid.finalbid = bid.bidprice
            closebid.save()
            bid.delete()
        except:
            closebid.bidder = listing.lister
            closebid.finalbid = listing.startingbids
            closebid.save()
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watch = Watchlist.objects.filter(listingid=listingid)
                watch.delete()
            else:
                pass
        except:
            pass
        try:
            comment = Comment.objects.filter(listingid=listingid)
            comment.delete()
        except:
            pass
        try:
            bid = Bid.objects.filter(listingid=listingid)
            bid.delete()
        except:
            pass
        try:
            closebidlist = Closebid.objects.get(listingid=listingid)
        except:
            closebid.lister = listing.lister
            closebid.bidder = listing.lister
            closebid.listingid = listingid
            closebid.finalbid = listing.startingbids
            closebid.save()
            closebidlist = Closebid.objects.get(listingid=listingid)
        listing.delete()
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount=None
        return render(request,"auctions/winner.html",{
            "closebidlist": closebidlist,
            "name": name,
            "watchcount":watchcount
        })   
    else:
        return redirect('index')


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
