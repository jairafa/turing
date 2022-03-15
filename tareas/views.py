from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.conf import settings
import pytz
import datetime as dt
from datetime import *
from django.db import connection
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import Max
from django.utils.translation import gettext as _

from tareas.models import masivos, masivos_file, tipo_masivo, masivos_file_adjunto
from tareas.forms import (
    cargarArchivoMasivo_Form,
    buscarPorNumero_nav_form,
    multiples_archivos_form,
)
from processes.clientes_bulk import clientes_bulk
from processes.cliente_dummy import get_system_user


def procesar_archivo_view(request, id):

    # user = auth.get_user(request)
    user = get_system_user()
    masivo_file = masivos_file.objects.get(id=id)
    if "clientes_bulk" in masivo_file.tipo_masivo.tarea:
        clientes_bulk(masivo_file, user)

    return redirect("tareas:verCargues", usuario_id=masivo_file.usuario_id)


class FormListView(FormMixin, ListView):
    def get(self, request, *args, **kwargs):
        # From FormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From ListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(
                ("Empty list and '%(class_name)s.allow_empty' is False.")
                % {"class_name": self.__class__.__name__}
            )

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ListarMasivosView(FormListView):
    template_name = "tareas/lista_masivos.html"
    model = masivos
    ordering = ("-id", "registro")
    paginate_by = 200
    context_object_name = "masivos"

    form_class = buscarPorNumero_nav_form
    # queryset = masivos.objects.all()[0:-10]

    def get_context_data(self, **kwargs):
        context = super(ListarMasivosView, self).get_context_data(**kwargs)
        context["form"] = buscarPorNumero_nav_form()
        return context

    def get_queryset(self):
        try:
            if self.request.method == "POST":
                tareaId = self.request.POST.get("pk")
                # usuario_id = self.request.POST.get('usuario_id')
            elif self.request.method == "GET":
                tareaId = self.request.GET.get("pk")
                # usuario_id = self.request.GET.get('usuario_id')
                if not tareaId or self.kwargs:
                    tareaId = self.kwargs["pk"]
                # if not usuario_id or self.kwargs:
                #   usuario_id = self.kwargs['usuario_id']
            elif self.kwargs:
                tareaId = self.kwargs["pk"]
                # usuario_id = self.kwargs['usuario_id']
        except NameError:
            tareaId = 0

        if int(tareaId) > 0:
            model = masivos.objects.filter(id=tareaId)
        else:
            ids = masivos.objects.values("id").distinct().order_by("-id")[:10]
            model = masivos.objects.filter(id__in=ids)

        return model


class ListarCarguesView(FormListView):
    template_name = "tareas/lista_cargues.html"
    model = masivos_file
    # ordering = ('-id')
    paginate_by = 20
    context_object_name = "cargues"
    # queryset = masivos.objects.all()[0:-10]
    form_class = buscarPorNumero_nav_form

    def get_context_data(self, **kwargs):
        context = super(ListarCarguesView, self).get_context_data(**kwargs)
        context["form"] = buscarPorNumero_nav_form()
        return context

    def get_queryset(self):

        print("a" * 10)
        print(self)

        try:
            # usuario_id = self.kwargs['usuario_id']
            user = User.objects.get(username__iexact="system_user")
            usuario_id = user.username
        except NameError:
            usuario_id = "0"

        try:
            if self.request.method == "POST":
                cargueId = self.request.POST.get("pk")
                # usuario_id = self.request.POST.get('usuario_id')
            elif self.request.method == "GET":
                cargueId = self.request.GET.get("pk")
                # usuario_id = self.request.GET.get('usuario_id')
                if not cargueId or self.kwargs:
                    # print("b" * 10)
                    # print(self.kwargs)
                    if "pk" in self.kwargs:
                        cargueId = self.kwargs["pk"]
                    else:
                        cargueId = 0
                if not usuario_id:
                    if "usuario_id" in self.kwargs:
                        usuario_id = self.kwargs["usuario_id"]
            elif self.kwargs:
                cargueId = self.kwargs["pk"]
            # print(f"usuario_id {usuario_id}")
        except NameError:
            cargueId = "0"

        # print(f"cargueId ({cargueId}) usuario_id ({usuario_id})")

        if usuario_id == "0":
            # print("1111")
            if int(cargueId) == 0:
                # print("2222")
                model = masivos_file.objects.get_queryset().order_by("-id")
            # print("3333")
            model = masivos_file.objects.filter(id=cargueId).order_by("-id")
        else:
            # print("4444")
            """
            return masivos_file.objects.all();
            ids = masivos_file.objects.values('id').distinct().order_by('-id')[:5]
            return masivos_file.objects.filter(id__in = ids)
            """
            model = masivos_file.objects.filter(usuario_id=usuario_id).order_by("-id")[:50]
        return model


class ListarAdjuntosView(LoginRequiredMixin, ListView):
    template_name = "tareas/lista_adjuntos.html"
    model = masivos_file_adjunto
    ordering = "-id"
    paginate_by = 20
    context_object_name = "adjuntos"
    # queryset = masivos.objects.all()[0:-10]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        modo = self.kwargs["modo"]
        # print(f"ListarAdjuntosView pk {pk} modo {modo}")
        if modo == "masivo_file_id":
            """
            mfi = masivos_file_adjunto.objects.filter(masivo_file_id = pk).order_by('-id')
            for m in mfi:
                print(f"masivo_file {m.masivo_file_id}")
            """
            return masivos_file_adjunto.objects.filter(masivo_file_id=pk).order_by("-id")
        if modo == "masivo_id":
            return masivos_file_adjunto.objects.filter(masivo_id=pk).order_by("-id")


class cargarArchivoMasivos(CreateView):
    model = masivos_file
    template_name = "tareas/cargar_archivo.html"
    form_class = cargarArchivoMasivo_Form
    success_url = "tareas:verCargues"

    def get_initial(self, *args, **kwargs):
        initial = super(cargarArchivoMasivos, self).get_initial(**kwargs)

        # user = auth.get_user(self.request)
        user = User.objects.get(username__iexact="system_user")
        initial = {"estado": "PendienteDeProcesar", "usuario": user}

        return initial

    def get(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        archivosForm = multiples_archivos_form()

        return self.render_to_response(
            self.get_context_data(
                form=form, archivosForm=archivosForm, titulo=_("Cargues Masivos")
            )
        )

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        archivosForm = multiples_archivos_form(
            self.request.POST or None, self.request.FILES or None
        )
        if form.is_valid() and archivosForm.is_valid():
            return self.form_valid(request, form, archivosForm)
        else:
            return self.form_invalid(form, archivosForm)

    def form_invalid(self, form, archivosForm):
        msg = "form (" + form.errors.as_text() + ")"
        msg += "Archivos (" + archivosForm.errors.as_text() + ")"
        msg = msg.replace("*", "")
        msg = msg.replace("__all__", "")
        return render(self.request, "base/elError.html", {"errors": msg})

    def form_valid(self, request, form, archivosForm):
        # elRadicado = crear.cleaned_data
        # user = auth.get_user(self.request)
        user = User.objects.get(username__iexact="system_user")

        masivo_file_data = form.cleaned_data
        # form = form.save(commit = False) #solicitar2Form.cleaned_data
        tipo_masivo = masivo_file_data["tipo_masivo"]
        # print('1111')

        # print(masivo_file_data)
        form.save()
        # print(masivo_file_data)

        res = masivos_file.objects.filter().aggregate(max_id=Max("pk"))
        masivo_file_id = res.get("max_id")

        # print(f"masivo_file_id {masivo_file_id}")
        # i=0
        # cantidadHojasPdf = 0
        # print('2222')
        if tipo_masivo.tiene_adjunto == "S":
            files = self.request.FILES.getlist("archivos")
            for f in files:
                # i += 1
                cargar_adjunto(user, masivo_file_id, f)

        procesar_archivo_view(request, masivo_file_id)

        return redirect("tareas:verCargues", usuario_id=user.username)


def cargar_adjunto(user, masivo_file_id, archivo):
    errores = ""
    registro = 0
    if "_" not in archivo.name:
        errores = "El nombre del archivo debe iniciar con "
        errores += "el numero de la fila seguido por un guión bajo (_)"
    else:
        inicio_name = archivo.name.split("_", 1)
        try:
            registro = int(inicio_name[0])
            if registro < 2:
                errores = "El numero del nombre del archivo debe ser mayor a uno"

        except ValueError:
            errores = "El nombre del archivo debe iniciar con el numero de la fila"

    if registro > 0 and len(errores) == 0:
        masivos_file_adjunto.objects.create(
            # id = adjunto_id,
            masivo_file_id=masivo_file_id,
            registro=registro,
            usuario_id=user.username,
            estado="pendiente de procesar",
            archivo=archivo,
        )
    else:
        masivos_file_adjunto.objects.create(
            # id = adjunto_id,
            masivo_file_id=masivo_file_id,
            usuario_id=user.username,
            estado="error",
            observaciones=errores,
            archivo=archivo,
        )


def load_estructura(request):
    # print(f"******load_estructura ajax request {request} *************" )
    if request.method == "POST":
        id_tipo_masivo = request.POST.get("id_tipo_masivo")
        campo = request.POST.get("campo")
    else:
        id_tipo_masivo = request.GET.get("id_tipo_masivo")
        campo = request.GET.get("campo")

    # print(f"ajax load_estructura id_tipo_masivo: {id_tipo_masivo}")

    tipoMasivo = tipo_masivo.objects.get(id=id_tipo_masivo)
    mensajes = []
    # mensajes.append("Estructura del Archivo de Cargue. Delimitador punto y coma (;)")
    mensajes.append(tipoMasivo.estructura)

    return render(request, "base/ajax_mensajes_n.html", {"mensajes": mensajes, "campo": campo})


def load_tiene_adjunto(request):
    # print(f"******load_estructura ajax request {request} *************" )
    if request.method == "POST":
        id_tipo_masivo = request.POST.get("id_tipo_masivo")
    else:
        id_tipo_masivo = request.GET.get("id_tipo_masivo")

    # print(f"ajax load_tiene_adjunto id_tipo_masivo: {id_tipo_masivo}")

    tipoMasivo = tipo_masivo.objects.get(id=id_tipo_masivo)
    return render(
        request,
        "base/ajax_clave_valor.html",
        {"clave": "tiene_adjunto", "valor": tipoMasivo.tiene_adjunto},
    )
