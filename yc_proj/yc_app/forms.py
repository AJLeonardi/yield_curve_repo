from django import forms
from django.utils import timezone


class FetchTreasuryDataForm(forms.Form):
    year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1950', 'max': '2022'}))
    month = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1', 'max': '12'}))
    day = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control validate', 'min': '1', 'max': '31'}))

    def __init__(self, *args, **kwargs):
        super(FetchTreasuryDataForm, self).__init__(*args, **kwargs)
        today = timezone.now()
        year = today.year
        self.fields['year'].initial = today.year
        self.fields['month'].initial = today.month
        self.fields['day'].initial = today.day