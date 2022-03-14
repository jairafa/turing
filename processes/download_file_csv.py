import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str


def download_file(file_name: str, s_path_file: str):
    with open(s_path_file, newline="") as file_csv:
        response = HttpResponse(file_csv, content_type="text/csv")
        content = "attachment; filename = {0}".format(file_name)
        response["content-Disposition"] = content
        return response
