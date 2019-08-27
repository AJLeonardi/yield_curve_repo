from django import forms
from django.forms import ModelForm, IntegerField, NumberInput, TextInput, Textarea, EmailInput, PasswordInput, DateTimeInput, SelectDateWidget, CheckboxInput, modelformset_factory, Select, RadioSelect
from django.utils import timezone


class FetchTreasuryDataForm(forms.Form):
    year = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1950', 'max': '2022'}))
    month = forms.CharField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1', 'max': '12'}))
    day = forms.CharField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1', 'max': '31'}))

    def __init__(self, *args, **kwargs):
        super(FetchTreasuryDataForm, self).__init__(*args, **kwargs)
        today = timezone.now()
        year = today.year
        self.fields['year'].initial = today.year
        self.fields['month'].initial = today.month
        self.fields['day'].initial = today.day