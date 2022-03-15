from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.admin import widgets
from django.forms import ModelForm
from django.utils import timezone

from datetime import date
from datetime import timedelta

from tareas.models import masivos_file
from tareas.views import *


class buscarPorNumero_nav_form(forms.Form):
    pk = forms.IntegerField(required=False, label="Numero")


class cargarArchivoMasivo_Form(forms.ModelForm):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "text/csv"}),
        required=True,
        label="Archivo csv/txt",
    )

    def __init__(self, *args, **kwargs):
        super(cargarArchivoMasivo_Form, self).__init__(*args, **kwargs)

        self.fields["estado"].widget = forms.HiddenInput()
        self.fields["tipo_masivo"].required = True
        self.fields["archivo"].required = True

    def clean_usuario_id(self):
        usuario_id = self.cleaned_data["usuario_id"]
        print(f"usuario_id: {usuario_id}" + "a" * 10)
        if not usuario_id:
            usuario_id = User.objects.get(username__iexact="system_user").username
        return usuario_id

    def clean(self, *args, **kwargs):
        if not self.cleaned_data["tipo_masivo"]:
            raise forms.ValidationError("Seleccione un Tipo de Cargue")

        if not self.cleaned_data["archivo"]:
            raise forms.ValidationError("Seleccione un Origen Archivo txt/csv")

        ext = self.cleaned_data["archivo"].name.split(".")[-1]
        if ext.lower() != "csv" and ext.lower() != "txt":
            raise forms.ValidationError("Seleccione un Origen Archivo txt/csv")

        return super(cargarArchivoMasivo_Form, self).clean(*args, **kwargs)

    class Meta:
        model = masivos_file

        fields = [
            "id",
            "tipo_masivo",
            "usuario_id",
            "estado",
            "archivo",
        ]

        labels = {
            "id": "No. Cargue",
            "tipo_masivo": "Cargue",
            "archivo": "Archivo a Procesar",
        }


class multiples_archivos_form(forms.Form):
    archivos = forms.FileField(
        label="Cargar Archivos Pdf/zip",
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "accept": "application/pdf, application/x-zip-compressed"}
        ),
        required=False,
    )

    class Meta:
        fields = ["archivos"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_archivos(self):
        archivos = self.cleaned_data["archivos"]
        if archivos:
            if archivos._size > settings.MAX_UPLOAD_SIZE:  # 40 Mg
                raise forms.ValidationError("El tamaño del archivo no debe superar los 80 Mg")
            return archivos
