from django import forms

class DonationRequestForm(forms.Form):
    donation_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    donation_message = forms.CharField(widget=forms.Textarea)