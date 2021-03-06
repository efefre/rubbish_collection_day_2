from django import forms
from city_detail.models import City
from schedule.models import RubbishType, RubbishDistrict


class UploadStreetsForm(forms.Form):
    file = forms.FileField(label="Plik csv")


class AddStreetsToCityForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), empty_label=None, label="Miejscowość"
    )
    streets = forms.CharField(widget=forms.Textarea, label="Ulica", required=False)

    extra_street = forms.CharField(widget=forms.TextInput,
                                   label="Ulica, która ma przecinek w nazwie",
                                   required=False)


class AddAddressToRubbishDistrictForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), label="Miejscowość"
    )

    rubbish_type = forms.ModelChoiceField(
        queryset=RubbishType.objects.all(), label="Frakcja śmieci"
    )

    rubbish_district = forms.ModelChoiceField(
        queryset=RubbishDistrict.objects.all(),
        label="Rejon odbioru odpadów"
    )

    streets = forms.CharField(widget=forms.Textarea, label="Ulice")


class AddDatesToRubbishDistrictForm(forms.Form):
    city_type = forms.ChoiceField(choices=[("", "---------"),
                                           ("gmina", "Gmina"),
                                           ("miasto", "Miasto")],
                                  label="Typ")

    rubbish_type = forms.ModelChoiceField(
        queryset=RubbishType.objects.all(),
        label="Frkacja śmieci",
    )
    rubbish_district = forms.ModelChoiceField(
        queryset=RubbishDistrict.objects.all(),
        label="Rejon odbioru odpadów",
    )

    dates = forms.CharField(widget=forms.Textarea,
                            label="Daty odbioru odpadów")
