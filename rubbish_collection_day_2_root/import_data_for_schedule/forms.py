from django import forms


class UploadStreetsForm(forms.Form):
    file = forms.FileField()
