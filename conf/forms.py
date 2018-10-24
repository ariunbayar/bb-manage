from django import forms


class BBSettingForm(forms.Form):
    username = forms.CharField(max_length=1000)
    client_key = forms.CharField(max_length=1000)
    client_secret = forms.CharField(max_length=1000)
    code = forms.CharField(max_length=1000)
    refresh_token = forms.CharField(max_length=1000)
    access_token = forms.CharField(max_length=1000)
