from django import forms
from .models import Rental


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ("start_date", "end_date")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
