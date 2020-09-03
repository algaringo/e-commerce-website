from django import forms

from .models import Listing, Bidding, Comment

class ListingForm(forms.ModelForm):
    class  Meta:
        model = Listing
        labels = {
            'productnames' : 'Listing Title',
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
            'bidprice' : ''
        }
        fields = [
            'bidprice'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            'comment' : ''
        }
        fields = [
            'comment'
        ]


