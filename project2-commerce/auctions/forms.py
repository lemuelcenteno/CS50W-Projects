from django import forms
from django.core.validators import MinValueValidator

from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "image_url", "starting_bid"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "bid_price",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]
