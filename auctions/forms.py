from django import forms

from .models import Listing, Bidding

class ListingForm(forms.ModelForm):
    class  Meta:
        model = Listing
        labels = {
            'productnames' : 'Product Name',
            'descriptions' : 'Description',
            'startingbids' : 'Starting Bid',
            'images' : 'Image URL',
            'category' : 'Category'
        }
        fields = [
            'productnames',
            'descriptions',
            'startingbids',
            'images',
            'category'
        ]

class BiddingForm(forms.ModelForm):
    class  Meta:
        model = Bidding
        labels = {
            'bidprice' : 'Bid'
        }
        fields = [
            'bidprice'
        ]
