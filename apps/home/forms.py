from django import forms

from apps.authentication.models import Company
from apps.home.models import Sklad


class ZakazForm(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            "obiem",
            "tovar",
            'company',
        )
        widgets = {
            "obiem": forms.NumberInput(attrs={'class': 'form-control'}),
            "tovar": forms.Select(attrs={'class': 'form-control'}),
            "company": forms.Select(attrs={'class': 'form-control'}),
            # "status": forms.Select(attrs={'class': 'form-control'}),
        }


class ZakazUpdateForm(forms.ModelForm):
    class Meta:
        model = Sklad
        fields = (
            '__all__'
        )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'address',
        )
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            # "city": forms.Select(attrs={'class': 'form-control'}),
            # "country": forms.Select(attrs={'class': 'form-control'}),
        }
