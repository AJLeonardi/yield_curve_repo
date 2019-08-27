from django import forms
from django.forms import ModelForm, IntegerField, NumberInput, TextInput, Textarea, EmailInput, PasswordInput, DateTimeInput, SelectDateWidget, CheckboxInput, modelformset_factory, Select, RadioSelect


class FetchTreasuryDataForm(ModelForm):
    year = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control validate'}))
    month = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    day = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
