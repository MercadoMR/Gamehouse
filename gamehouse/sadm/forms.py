
#Formularios para el jugador
from django import forms
from django.forms import models
from .models import MatrizJuegos,TfIdf

class MatrizJuegosForm(forms.ModelForm):
    class Meta:
        model=MatrizJuegos
        exclude=('juego',)

class TfIdfForm(forms.ModelForm):
    class Meta:
        model= TfIdf
        fields=['vector']
        labels={
            'vector':'Vector de caracteristicas',}