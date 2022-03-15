from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from tareas.views import (
    ListarMasivosView,
    cargarArchivoMasivos,
    ListarCarguesView,
    load_estructura,
    procesar_archivo_view,
    ListarAdjuntosView,
    load_tiene_adjunto,
)
from processes.download_file_csv import download_bulk

urlpatterns = [
    path("download/<int:carga_id>", download_bulk, name="descargar_bulk_csv"),
    re_path(r"^consultar/(?P<pk>\d+)/$", ListarMasivosView.as_view(), name="verUnaTarea"),
    re_path(r"^consultar/$", ListarMasivosView.as_view(), name="verTareas"),
    re_path(
        r"^consultarAdjuntos/(?P<pk>\d+)/(?P<modo>[-\_\w]+)/$",
        ListarAdjuntosView.as_view(),
        name="verUnAdjunto",
    ),
    re_path(
        r"^consultarCargues/(?P<usuario_id>[-\_\w]+)/$",
        ListarCarguesView.as_view(),
        name="verCargues",
    ),
    re_path(r"^consultarCargues/$", ListarCarguesView.as_view(), name="verCarguesFiltro"),
    re_path(r"^cargarArchivos/$", cargarArchivoMasivos.as_view(), name="cargar_archivos"),
    re_path(r"^procesarArchivo/(?P<id>\d+)/$", procesar_archivo_view, name="procesar_archivo"),
    re_path("^ajax/load-estructura/", load_estructura, name="ajax_estructura"),
    re_path("^ajax/load-tiene_adjunto/", load_tiene_adjunto, name="ajax_adjunto"),
]
