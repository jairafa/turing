from ast import Str
import io
import csv
from cliente.models import category


def migrate_category(s_file_path_name: str) -> bool:
    termina: bool = True
    numReg: int = 0
    regOk: int = 0
    regError: int = 0
    regBlancos: int = 0
    mensaje: str = "Archivo " + s_file_path_name + " procesado."
    with open(s_file_path_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        try:
            for row in reader:
                numReg += 1
                category_name: str = ""
                try:
                    category_name = row[0]
                except NameError:
                    regBlancos += 1
                if len(category_name) > 0:
                    mensaje_category: str = "numReg (" + str(numReg)
                    mensaje_category += ") category_name (" + category_name + ")"
                    if category.objects.filter(name=category_name).exists():
                        print(f"{mensaje_category} ya existe, no se crea")
                        regOk += 1
                    else:
                        category.objects.create(name=category_name)
                        print(f"{mensaje_category} creada correctamente")
                        regError += 1
        except csv.Error as e:
            mensaje = "|linea " + str(reader.line_num) + " " + str(e)
            termina = False
            regError += 1
        except IndexError as e:
            mensaje = "|linea " + str(reader.line_num) + " " + str(e)
            termina = False
            regError += 1
    mensaje += "| regCsvOk " + str(regOk) + " regCsvError " + str(regError)
    mensaje += " regBlancos " + str(regBlancos)
    mensaje += " --> TotRegCsv " + str(regOk + regError + regBlancos)

    print(mensaje)
    return termina
