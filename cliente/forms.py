from django import forms
from .models import territorial, category, cliente
from django.utils.translation import gettext_lazy as _

from processes.cliente_dummy import get_system_user


class client_filter_form(forms.Form):
    cliente_id = forms.IntegerField(required=False, label=_("Cliente ID"))
    name = forms.CharField(required=False, label=_("Nombre"))
    city = forms.ModelChoiceField(
        required=False, label="Ciudades", queryset=territorial.objects.filter(territorial_type="C")
    )
    departament = forms.ModelChoiceField(
        required=False,
        label=_("Departamentos"),
        queryset=territorial.objects.filter(territorial_type="D"),
    )
    category = forms.ModelChoiceField(
        required=False, label=_("Categorias"), queryset=category.objects.all()
    )
    fecha_ini = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False,
        label=_("Fecha Crea Inicio"),
    )
    fecha_fin = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
        required=False,
        label=_("Fecha Crea Fin"),
    )
    order_by_id = forms.ChoiceField(
        label=_("Ordenamiento por id"),
        choices=(
            (
                "asc",
                "Ascendente",
            ),
            (
                "desc",
                "Descendente",
            ),
        ),
        initial="asc",
    )
    generar_xls = forms.ChoiceField(
        choices=(
            (
                "S",
                "Generar Excell",
            ),
            (
                "N",
                "Ver Datos",
            ),
        ),
        initial="N",
    )


class client_form(forms.ModelForm):
    country = forms.ModelChoiceField(
        required=True, label=_("Paises"), queryset=territorial.objects.filter(territorial_type="P")
    )
    departament = forms.ModelChoiceField(
        required=True,
        label="Departamentos",
        queryset=territorial.objects.filter(territorial_type="D"),
    )
    city = forms.ModelChoiceField(
        required=True,
        label=_("Ciudades"),
        queryset=territorial.objects.filter(territorial_type="C"),
    )
    category = forms.ModelChoiceField(
        required=True, label=_("Categorias"), queryset=category.objects.all()
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
            "name": _("Nombre"),
            "category": _("Categoría"),
            "country": _("Pais"),
            "departament": _("Departamento"),
            "city": _("Ciudad"),
        }


class client_desable_form(forms.ModelForm):
    disabled_fields = (
        "name",
        "category",
        "country",
        "departament",
        "city",
    )

    class Meta:
        model = cliente
        fields = [
            "id",
            "name",
            "category",
            "country",
            "departament",
            "city",
            "is_active",
        ]
        labels = {
            "name": _("Nombre"),
            "category": _("Categoría"),
            "country": _("Pais"),
            "departament": _("Departamento"),
            "city": _("Ciudad"),
        }

    def __init__(self, *args, **kwargs):
        super(client_desable_form, self).__init__(*args, **kwargs)
        self.fields["is_active"].widget = forms.HiddenInput()
        for field in iter(self.fields):
            if field != "id":
                self.fields[field].widget.attrs.update({"class": "form-control"})
        for field in self.disabled_fields:
            self.fields[field].disabled = True
