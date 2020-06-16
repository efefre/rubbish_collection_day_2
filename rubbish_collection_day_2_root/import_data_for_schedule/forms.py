from django import forms
from city_detail.models import City


class UploadStreetsForm(forms.Form):
    file = forms.FileField()


class AddStreetsToCityForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label=None)
    streets = forms.CharField(widget=forms.Textarea)
