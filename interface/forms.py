from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ArgoSearchForm(forms.Form):
    data_type = forms.TextInput()
    platform_number = forms.IntegerField()
    # cycle = forms.IntegerField()
