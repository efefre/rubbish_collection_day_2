from django import forms
from city_detail.models import Address


class ChooseAddress(forms.ModelForm):
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
