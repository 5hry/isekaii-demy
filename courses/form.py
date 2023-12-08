from django import forms
from .models import Rating

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=5, required=True)
    comment = forms.CharField(widget=forms.Textarea, required=True)