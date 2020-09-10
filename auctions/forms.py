from django import forms
from .models import Listing, Bidding, Comment, Category

CATEGORY = Category.objects.all().values_list('name', 'name')
CATEGORY1 = {
    ('', '')
}

categories = []

for item in CATEGORY:
    categories.append(item)
for item in CATEGORY1:
    categories.append(item)

class ListingForm(forms.ModelForm):
    class  Meta:
        model = Listing
        labels = {
            'productnames' : 'Productname',
            'descriptions' : 'Description',
            'startingbids' : 'Starting Bids',
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
        widgets = {
            'category': forms.Select(choices=categories, attrs={'class': 'form-control'})
        }
    

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


