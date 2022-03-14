from ast import Str
import io
import csv
from cliente.models import territorial


def migrate_territorial(s_file_path_name: str) -> bool:
    termina: bool = True
    numReg: int = 0
    regOk: int = 0
    regError: int = 0
    mensaje: str = "Archivo " + s_file_path_name + " procesado."
    with open(s_file_path_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        try:
            for row in reader:
                numReg += 1
                reg_is_ok: bool = True
                territorial_id: str = ""
                territorial_name: str = ""
                territorial_type: str = ""
                territorial_parent_id: str = ""
                if numReg > 1:
                    try:
                        territorial_id = row[0]
                        territorial_name = row[1]
                        territorial_type = row[2]
                        territorial_parent_id = row[3]
                    except NameError:
                        reg_is_ok = False

                    if reg_is_ok:
                        mensaje_territorial: str = "numReg (" + str(numReg)
                        mensaje_territorial += ") territorial_name (" + territorial_name + ")"
                        if territorial.objects.filter(name=territorial_name).exists():
                            print(f"{mensaje_territorial} ya existe, no se crea")
                            regError += 1
                        else:
                            territorial.objects.create(
                                id=territorial_id,
                                name=territorial_name,
                                territorial_type=territorial_type,
                                parent_id=territorial_parent_id,
                            )
                            print(f"{mensaje_territorial} creada correctamente")
                            regOk += 1
                    else:
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
    mensaje += " --> TotRegCsv " + str(regOk + regError)

    print(mensaje)
    return termina
