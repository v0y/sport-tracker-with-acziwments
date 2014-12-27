# encoding: utf-8

from django import forms
from django.forms.models import ModelForm

from .models import Health


def _str_to_float(string):
    try:
        number = float(string.replace(',', '.'))
    except ValueError:
        return None
    return number


class HealthForm(ModelForm):
    related_date = forms.DateField(
        label='Date', input_formats=['%d-%m-%Y'])
    weight = forms.CharField(required=False)
    fat = forms.CharField(label='Body fat', required=False)
    water = forms.CharField(label='Body water', required=False)

    class Meta:
        button_text = 'Save'
        exclude = ('user',)
        model = Health
        name = 'Add weight data'

    def clean(self):
        cd = super(HealthForm, self).clean()
        weight = cd.get('weight')
        fat = cd.get('fat')
        water = cd.get('water')
        if not any([weight, fat, water]):
            raise forms.ValidationError(
                'At least one of "Weight", "Body fat", "Body water" '
                'is required'
            )
        return cd

    def clean_related_date(self):
        date = self.cleaned_data.get('related_date')
        # check, if entry for this date already exist
        current_pk = self.instance.pk
        if Health.objects.filter(related_date=date).exclude(pk=current_pk):
            raise forms.ValidationError('There is existing data for this date')
        return date

    def clean_weight(self):
        return _str_to_float(self.cleaned_data.get('weight'))

    def clean_fat(self):
        return _str_to_float(self.cleaned_data.get('fat'))

    def clean_water(self):
        return _str_to_float(self.cleaned_data.get('water'))
