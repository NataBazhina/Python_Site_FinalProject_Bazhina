from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("text", "rating")
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "").strip()
        if not text:
            raise forms.ValidationError("Review text cannot be empty.")
        return text
