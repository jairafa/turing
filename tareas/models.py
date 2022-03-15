from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class masivos(models.Model):
    tarea = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Tarea"))
    registro = models.IntegerField(verbose_name=_("registro"))  # AutoField?
    resultado = models.CharField(
        max_length=4000, blank=True, null=True, verbose_name=_("Resultado")
    )
    fecha = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Fecha"))
    estado = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Estado"))
    usuario_id = models.CharField(max_length=32, blank=True, null=False, verbose_name=_("Usuario"))
    identificador = models.CharField(
        max_length=25, blank=True, null=False, verbose_name=_("Identificador")
    )
    tipo_identificador = models.CharField(
        max_length=25, blank=True, null=False, verbose_name=_("Tipo Identificador")
    )
    masivo_file_id = models.IntegerField()

    class Meta:
        ordering = ["-id", "tarea"]

    def __str__(self):
        return "{} ".format(self.nombre)

    @staticmethod
    def get_queryset(self):
        # print(f"params {self.request}")
        id = self.request.get("id")
        return masivos.objects.filter(id=id)


class tipo_masivo(models.Model):  # radicaciones_tipo_masivo
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Nombre"))
    activo = models.CharField(max_length=1)
    tiene_adjunto = models.CharField(
        max_length=1
    )  # Para desplegar en la pantalla de cargue de archivos el botón poara cargar adjuntos
    tarea = models.CharField(max_length=120, blank=True, null=True, verbose_name=_("Tarea"))
    estructura = models.CharField(max_length=2000, verbose_name=_("Estructura"))

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return "{} ".format(self.nombre)


class masivos_file(models.Model):
    usuario_id = models.CharField(max_length=32, blank=True, null=False)
    fecha = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Fecha"))
    estado = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Estado"))
    tipo_masivo = models.ForeignKey(tipo_masivo, models.DO_NOTHING)
    observaciones = models.CharField(
        max_length=2000, blank=True, null=True, verbose_name=_("Observaciones")
    )
    archivo = models.FileField(
        upload_to="reports/%Y/%m/", blank=True, null=True, verbose_name=_("Archivo")
    )
    masivo_id = models.IntegerField(blank=True, null=True)  # AutoField?

    class Meta:
        ordering = ["-id"]

    def getNombreArchivo(this):
        ruta = this.archivo.name.split("/")
        for nombre in ruta:
            if "." in nombre:
                return nombre
        return ruta

    def getRutaArchivo(this):
        return settings.MEDIA_ROOT + this.archivo.name

    def getExtension(this):
        extension = this.archivo.name.split(".")[1]
        return extension.lower()

    def __str__(self):
        return "{} {} {}".format(self.id, self.getNombreArchivo(), self.estado)


class masivos_file_adjunto(models.Model):
    # id = models.IntegerField(primary_key=True , blank=True, null=False)  # AutoField?
    masivo_file = models.ForeignKey(masivos_file, models.DO_NOTHING)
    registro = models.IntegerField()  # AutoField?
    usuario_id = models.CharField(max_length=32, blank=True, null=False, verbose_name=_("Usuario"))
    fecha = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_("Fecha"))
    estado = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Estado"))
    observaciones = models.CharField(
        max_length=2000, blank=True, null=True, verbose_name=_("Observaciones")
    )
    archivo = models.FileField(
        upload_to="reports/adjuntos/%Y/%m/", blank=True, null=True, verbose_name=_("Archivo")
    )
    masivo_id = models.IntegerField(blank=True, null=False)
    radicado_id = models.IntegerField(blank=True, null=False)

    class Meta:
        managed = False
        ordering = ["-id"]

    def getNombreArchivo(this):
        ruta = this.archivo.name.split("/")
        for nombre in ruta:
            if "." in nombre:
                return nombre
        return ruta

    def getRutaArchivo(this):
        return settings.MEDIA_ROOT + this.archivo.name

    def getExtension(this):
        extension = this.archivo.name.split(".")[1]
        return extension.lower()

    def __str__(self):
        return "{} {} {}".format(self.id, self.getNombreArchivo(), self.estado)
