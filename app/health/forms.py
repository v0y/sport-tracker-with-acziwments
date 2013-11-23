# encoding: utf-8

from django import forms
from django.forms.models import ModelForm

from .models import Health


class HealthForm(ModelForm):
    related_date = forms.CharField(label=u"Data pomiaru")
    weight = forms.CharField(label=u'Waga (kg)', required=False)
    fat = forms.CharField(label=u'Tłuszcz (%)', required=False)
    water = forms.CharField(label=u'Woda (%)', required=False)

    class Meta:
        button_text = u"Zapisz"
        exclude = ('user',)
        model = Health
        name = u"Dodaj pomiar wagi"

    def clean(self):
        cd = super(HealthForm, self).clean()
        weight = cd.get('weight')
        fat = cd.get('fat')
        water = cd.get('water')
        datas = [weight, fat, water]
        if not [data for data in datas if type(data) in (float, int)]:
            raise forms.ValidationError(
                u"Conajmniej jedno z pól 'Waga', 'Tłuszcz', 'Woda' musi "
                u"zostać wypełnione")
        return cd

    def clean_related_date(self):
        date = self.cleaned_data.get('related_date')
        # change format
        try:
            ds = date.split('-')
            date = '%s-%s-%s' % (ds[2], ds[1], ds[0])
        except IndexError:
            pass
        # check, if entry for this date already exist
        current_pk = self.instance.pk
        if Health.objects.filter(related_date=date).exclude(pk=current_pk):
            raise forms.ValidationError(
                u"Dla tej daty istnieje już pomiar wagi")
        return date

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        try:
            weight = float(weight.replace(',', '.'))
        except ValueError:
            pass
        return weight
    
    def clean_fat(self):
        fat = self.cleaned_data.get('fat')
        try:
            fat = float(fat.replace(',', '.'))
        except ValueError:
            pass
        return fat
    
    def clean_water(self):
        water = self.cleaned_data.get('water')
        try:
            water = float(water.replace(',', '.'))
        except ValueError:
            pass
        return water
