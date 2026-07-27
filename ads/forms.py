from django import forms
from datetime import date
from .models import Ad

class AdForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False,
        label="Дата начала аренды",
        input_formats=["%Y-%m-%d"],
    )
    end_date = forms.DateField(
        required=False,
        label="Дата окончания аренды",
        input_formats=["%Y-%m-%d"],
    )
    image = forms.ImageField(
        required=False,
        label="Фото объявления",
    )

    class Meta:
        model = Ad
        fields = ["title", "description", "price", "location", "contact", "start_date", "end_date", "image"]

        def clean(self):
            super().clean()
            start = self.cleaned_data.get("start_date")
            end = self.cleaned_data.get("end_date")

            if start and end and start > end:
                raise forms.ValidationError("Дата начала не может быть позже даты окончания.")

            return self.cleaned_data
