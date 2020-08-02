from django import forms
from city_detail.models import City
from schedule.models import RubbishType, RubbishDistrict


class UploadStreetsForm(forms.Form):
    file = forms.FileField(label="Plik csv")


class AddStreetsToCityForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), empty_label=None, label="Miejscowość"
    )
    streets = forms.CharField(widget=forms.Textarea, label="Ulica")


class AddAddressToRubbishDistrictForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(o.pk, o.name) for o in City.objects.all()]
        self.fields["city"] = forms.ChoiceField(
            choices=tuple([("", "---------")] + list(choices)),
        )
        self.fields["city"].label = "Miejscowość"
        self.fields["rubbish_district"] = forms.ChoiceField(
            choices=tuple([("", "---------")])
        )
        self.fields["rubbish_district"].label = "Rejon odbioru odpadów"

    city = forms.ModelChoiceField(
        queryset=City.objects.all()
    )

    rubbish_type = forms.ModelChoiceField(
        queryset=RubbishType.objects.all(), label="Frakcja śmieci"
    )

    rubbish_district = forms.ModelChoiceField(
        queryset=RubbishDistrict.objects.all(),
    )
    streets = forms.CharField(widget=forms.Textarea, label="Ulice")

class AddDatesToRubbishDistrictForm(forms.Form):
    rubbish_district = forms.ModelChoiceField(
        queryset=RubbishDistrict.objects.all(),
        empty_label=None,
        label="Rejon odbioru odpadów",
    )
    dates = forms.CharField(widget=forms.Textarea, label="Daty odbioru odpadów")
