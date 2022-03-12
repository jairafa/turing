from django import forms
from .models import territorial, category, cliente

from tareas.procesos.cliente_dummy import get_system_user


class client_filter_form(forms.Form):
    cliente_id = forms.IntegerField(required=False, label="Cliente ID")
    name = forms.CharField(required=False, label="Nombre")
    city = forms.ModelChoiceField(
        required=False, label="Ciudades", queryset=territorial.objects.filter(territorial_type="C")
    )
    departament = forms.ModelChoiceField(
        required=False,
        label="Departamentos",
        queryset=territorial.objects.filter(territorial_type="D"),
    )
    category = forms.ModelChoiceField(
        required=False, label="Categorias", queryset=category.objects.all()
    )


class client_form(forms.ModelForm):
    country = forms.ModelChoiceField(
        required=True, label="Paises", queryset=territorial.objects.filter(territorial_type="P")
    )
    departament = forms.ModelChoiceField(
        required=True,
        label="Departamentos",
        queryset=territorial.objects.filter(territorial_type="D"),
    )
    city = forms.ModelChoiceField(
        required=True, label="Ciudades", queryset=territorial.objects.filter(territorial_type="C")
    )
    category = forms.ModelChoiceField(
        required=True, label="Categorias", queryset=category.objects.all()
    )

    def clean_user_created(self):
        user_created = self.cleaned_data["user_created"]
        if not user_created:
            user_created = get_system_user()
        return user_created

    class Meta:
        model = cliente
        fields = [
            "name",
            "category",
            "country",
            "departament",
            "city",
            "user_created",
        ]
        labels = {
            "name": "Nombre",
            "category": "Categoría",
            "country": "Pais",
            "departament": "Departamento",
            "city": "Ciudad",
        }
