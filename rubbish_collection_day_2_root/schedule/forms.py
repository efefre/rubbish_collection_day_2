from django import forms
from city_detail.models import Address


class ChooseAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(o.city, o.city) for o in Address.objects.all()]
        self.fields["city"] = forms.ChoiceField(
            choices=tuple([("", "---------")] + list(choices))
        )
        self.fields["city"].label = "Wybierz miejscowość"

    class Meta:
        model = Address
        fields = (
            "city",
            "street",
        )
        labels = {
            "street": "Wybierz ulicę",
        }
        widgets = {
            "city": forms.Select(attrs={"class": "form-control"}),
            "street": forms.Select(attrs={"class": "form-control"}),
        }
