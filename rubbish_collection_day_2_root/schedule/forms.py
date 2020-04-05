from django import forms
from city_detail.models import Address


class ChooseAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("city", "street")
        labels = {
            "city": "Wybierz miejscowość",
            "street": "Wybierz ulicę",
        }
