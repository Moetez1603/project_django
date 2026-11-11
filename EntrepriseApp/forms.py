from django import forms

from .models import Entreprise


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        exclude = ['created_at', 'updated_at']
