from django import forms
from city_detail.models import Address, City


class ChooseAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(o.name, o.name) for o in City.objects.all()]
        self.fields["city"] = forms.ChoiceField(
            choices=tuple([("", "---------")] + list(choices))
        )
        self.fields["city"].label = "Wybierz miejscowość"
        self.fields["city"].widget.attrs["class"] = "form-control"

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
            "street": forms.Select(attrs={"class": "form-control"}),
        }
