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
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), empty_label=None, label="Miejscowość"
    )
    rubbish_type = forms.ModelChoiceField(
        queryset=RubbishType.objects.all(), empty_label=None, label="Frakcja śmieci"
    )
    rubbish_districy = forms.ModelChoiceField(
        queryset=RubbishDistrict.objects.all(),
        empty_label=None,
        label="Rejon odbioru odpadów",
    )
    streets = forms.CharField(widget=forms.Textarea, label="Ulice")
