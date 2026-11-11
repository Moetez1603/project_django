from django import forms

from .models import Vehicule


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        exclude = ['created_at', 'updated_at']
