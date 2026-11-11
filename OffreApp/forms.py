from django import forms

from .models import Offre


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        exclude = ['date_proposition', 'created_at', 'updated_at']
