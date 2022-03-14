# from datetime import *
import datetime
from django.conf import settings


class UtilCsv:
    file_name = None
    fCsv = None

    def __init__(self, new_file_name: str):
        # print('x' * 20)
        self.ruta_csv_inicio = str(settings.BASE_DIR).replace("\\", "/") + "/reports/"
        self.file_name = new_file_name.replace(".txt", ".csv")
        if self.file_name:
            self.file_name = self.ruta_csv_inicio + self.file_name
            self.fCsv = open(self.file_name, "w")

        # print(f"Destino: {self.file_name}")

        titulos = {
            "id": "Id",
            "name": "Cliente",
            "departament": "Departamento",
            "city": "Ciudad",
            "category": "Categoria",
            "user_created": "Creador",
            "created_at": "F Crea",
        }
        self.write(titulos)

    def get_name(self):
        return self.file_name

    def write(self, line):
        self.fCsv.write(
            "{};{};{};{};{};{};{}\n".format(
                line["id"],
                line["name"],
                line["departament"],
                line["city"],
                line["category"],
                line["user_created"],
                line["created_at"],
            )
        )

    def cerrar_csv(self):
        self.fCsv.close()
