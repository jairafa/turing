from django import forms
from .models import cliente


class solicitar1_Form(forms.ModelForm):
    class Meta:
        model = cliente
