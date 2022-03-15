import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from tareas.models import masivos_file


def download_file(file_name: str, s_path_file: str):
    with open(s_path_file, newline="") as file_csv:
        response = HttpResponse(file_csv, content_type="text/csv")
        content = "attachment; filename = {0}".format(file_name)
        response["content-Disposition"] = content
        return response


def download_bulk(request, carga_id: int):
    mf = masivos_file.objects.get(id=carga_id)
    file_name: str = mf.getNombreArchivo()
    s_path_file: str = mf.getRutaArchivo()
    with open(s_path_file, newline="") as file_csv:
        response = HttpResponse(file_csv, content_type="text/csv")
        content = "attachment; filename = {0}".format(file_name)
        response["content-Disposition"] = content
        return response
