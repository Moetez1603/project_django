from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Entreprise, Utilisateur


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        exclude = ['created_at', 'updated_at']


class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ('email', 'telephone', 'role')