from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from datetime import datetime
from django.utils.timezone import now


from .models import User, Listing, Bidding, Watchlist, Closebid, Comment, Category

from .forms import ListingForm, BiddingForm, CommentForm

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
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    if request.method == "POST":
        if form.is_valid():
            now = datetime.now()                                                #save date created with current timezone
            fs = form.save(commit=False)
            fs.lister = request.user                                            #save info not listed at forms.py
            fs.created = now
            fs.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create.html", {
            'form': form,
            'creator': creator,
            'watchcount': watchcount
        })

def listingpage(request,id):
    listing = Listing.objects.get(id=id)
    comment = Comment.objects.filter(listingid=id)
    try:
        cform = CommentForm(request.POST or None)
        bidform = BiddingForm(request.POST or None)
    except:
        return redirect('index')
    if request.user.username:
        try:
            if Watchlist.objects.get(watcher=request.user.username, listingid=id):
                added=True
        except:
            added = False
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount=None
        try:
            ccount = Comment.objects.filter(listingid=id)
            ccount = len(ccount)
        except:
            ccount = len(ccount)
        try:

            if listing.lister == request.user.username :
                lister = True
            else:
                lister = False
        except:
            return redirect('index')
    else: 
        ccount = Comment.objects.filter(listingid=id)
        ccount = len(ccount)
        added = False
        lister = False
        watchcount = None
    try:
        bid = Bidding.objects.filter(listingid=id)
        bidcount = len(bid)
        listing = Listing.objects.get(id=id)
    except:
        bicount = None
    return render(request, "auctions/listing.html", {
        'object': listing,
        'added': added,
        'bidform': bidform,
        "watchcount": watchcount,
        "error":request.COOKIES.get('error'),
        "success":request.COOKIES.get('success'),
        "bidcount": bidcount,
        "lister": lister,
        'cform': cform,
        "comment": comment,
        "ccount": ccount
    })

@login_required
def addwatch(request, id):
    if request.user.username:
        listing = Listing.objects.get(id=id)
        watchers = Watchlist(watcher = request.user.username, listingid = id)
        watchers.lister = listing.lister
        watchers.finalbid = listing.startingbids
        watchers.productnames = listing.productnames
        watchers.images = listing.images
        watchers.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
def removewatch(request,id):
    if request.user.username:
        try:
            Watchlist.objects.filter(listingid=id).delete()
            return redirect('listingpage', id=id)
        except:
            return redirect('listingpage', id=id)
    else:
        return redirect('index')

@login_required
def watchlist(request):
    try:
        watchlist = Watchlist.objects.filter(watcher=request.user.username)
        closebid = Closebid.objects.filter(bidder=request.user.username)
        watchcount = len(watchlist)                                                 #count how many rows in table Watchlist using len()                                    
    except:
        watchcount = None
    try:
        bidwincount = Closebid.objects.filter(bidder = request.user.username)
        bidwincount = len(bidwincount)
    except:
        binwincoun = None
    try:
        if Watchlist.objects.get(listingid=listingid):
            closed = True
        else:
            closed = False
    except:
        closed = False
    return render(request, "auctions/watchlist.html", {
        'object': watchlist,
        "watchcount": watchcount,
        "closedbid": closebid,
        "closed" : closed,
        "bidwincount": bidwincount
    })

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
            response.set_cookie('success','Successful Bid! Your bid is currently the highest bid.', max_age=1)
            return response
        else:
            response = redirect('listingpage', id=listingid)
            response.set_cookie('error','Your bid must be higher than the current price!', max_age=1)
            return response
    else:
        return redirect('index')
        
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
        closebid.productnames = listing.productnames
        closebid.images = listing.images
        closebid.category = listing.category
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
            closebid.productnames = listing.productnames
            closebid.images = listing.images
            closebid.category = listing.category
            closebid.save()
            closebidlist = Closebid.objects.get(listingid=listingid)
        listing.delete()
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount = None
        return render(request,"auctions/winner.html",{
            "closebidlist": closebidlist,
            "name": name,
            "watchcount":watchcount
        })   
    else:
        return redirect('index')

@login_required
def closed(request, listingid):
    closed = Closebid.objects.get(listingid=listingid)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, "auctions/closed.html", {
        "object": closed,
        "watchcount": watchcount
    })

@login_required
def comment(request, listingid):
    if request.method == "POST":
        comment = Comment.objects.all()
        cform = CommentForm(request.POST or None)
        if cform.is_valid():
            now = datetime.now()                                               
            fs = cform.save(commit=False)   
            fs.listingid = listingid
            fs.user = request.user.username                               
            fs.time = now
            fs.save()
        return redirect('listingpage', id=listingid)
    else:
        return redirect('index') 

def category(request):
    category = Category.objects.all()
    closedbid = Closebid.objects.all()
    try:
        if Watchlist.objects.get(listingid=listingid):
            closed = True
        else:
            closed = False
    except:
        closed = False
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, "auctions/categories.html", {
        "object": category,
        "watchcount": watchcount,
        "closed": closed,
        "closedbid": closedbid
    })

def categorylistings(request, cats):
    category_posts = Listing.objects.filter(category=cats)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, 'auctions/categorylistings.html', {
        'cats': cats,
        'category_posts': category_posts,
        'watchcount': watchcount
    })

def allclosed(request):
    closedlist = Closebid.objects.all()
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, 'auctions/allclosed.html', {
        'closedlist': closedlist,
        'watchcount': watchcount
    })

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
