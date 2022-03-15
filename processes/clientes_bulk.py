import io
import csv
from datetime import timedelta
from datetime import *
from datetime import datetime
from django.conf import settings

from tareas.models import masivos, tipo_masivo, masivos_file, masivos_file_adjunto
from cliente.models import cliente, territorial, category


def clientes_bulk(masivo_file, user):
    termina: bool = True
    numReg: int = 0
    regUpdateOk: int = 0
    regAddOk: int = 0
    regError: int = 0

    with open(masivo_file.getRutaArchivo(), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        mensaje: str = "Archivo csv procesado."

        try:
            masivo_file.estado = "ok"
            masivo_file.observaciones = ""
            list_add = []
            list_update = []
            for row in reader:
                estado: str = ""

                if len(row) > 0:
                    numReg = numReg + 1
                    if numReg > 1:
                        # print (f"numReg {numReg} row 0 ({row[0]}) 1 ({row[1]}) 2 ({row[2]}) ")
                        name = row[0]
                        category_id = row[1]
                        city_id = row[2]
                        estadoSolicitud = ""

                        if not name:
                            estadoSolicitud += "|Falta el nombre del cliente"
                        if not category_id:
                            estadoSolicitud += "|Falta el identificador de la categoria"
                        else:
                            if not category_id.isdigit():
                                estadoSolicitud += "|La categoria debe ser un numero entero"
                            elif int(category_id) < 1 or int(category_id) > 12:
                                estadoSolicitud += (
                                    "|La categoria (" + category_id + ") debe estar entre 1 y 12"
                                )

                        if not city_id:
                            estadoSolicitud += "|Falta el identificador de la ciudad"
                        else:
                            if not city_id.isdigit():
                                estadoSolicitud += "|La ciudad debe ser un numero entero"
                            elif int(city_id) < 5 or int(city_id) > 10:
                                estadoSolicitud += (
                                    "|La ciudad (" + city_id + ") debe estar entre 5 y 10"
                                )

                        if len(estadoSolicitud) == 0:
                            if cliente.objects.filter(name=name).exists():
                                regUpdateOk += 1
                                for client in cliente.objects.filter(name__icontains=name):
                                    client.category_id = category_id
                                    client.city_id = city_id
                                    departamento = territorial.objects.get(id=city_id)
                                    client.departament_id = departamento.id
                                    client.country_id = departamento.parent_id
                                    list_update.append(client)
                            else:
                                regAddOk += 1
                                departamento = territorial.objects.get(id=city_id)
                                client = cliente(
                                    name=name,
                                    category_id=category_id,
                                    city_id=city_id,
                                    departament_id=departamento.id,
                                    country_id=departamento.parent_id,
                                )
                                list_add.append(client)
                            estado = "Ok"
                        else:
                            estadoSolicitud += "|Paramentros del registro incorrectos"
                            estado = "ERROR"
                            regError = regError + 1

            cliente.objects.bulk_create(list_add)
            cliente.objects.bulk_update(
                list_update, ["name", "category_id", "city_id", "departament_id", "country_id"]
            )

            masivo = masivos.objects.create(
                # id = masivoId,
                tarea=masivo_file.tipo_masivo.tarea,
                registro=numReg,
                resultado=estadoSolicitud,
                # identificador = radicado_id,
                tipo_identificador="cliente",
                usuario_id=user.username,
                estado=estado,
                masivo_file_id=masivo_file.id,
            )
            # print(f"+++++++Genero masivo.id ({masivo.id})++++++")
            masivo_file.masivo_id = masivo.id
            masivo_file.save(update_fields=["masivo_id"])

        except csv.Error as e:
            mensaje = "|linea " + str(reader.line_num) + " " + str(e)
            # masivo_file.observaciones = masivo_file.observaciones + mensaje
            masivo_file.estado = "error"
            termina = False
        except IndexError as e:
            mensaje = "|linea " + str(reader.line_num) + " " + str(e)
            # masivo_file.observaciones = masivo_file.observaciones + mensaje
            masivo_file.estado = "error"
            termina = False

    mensaje += "| regAddOk " + str(regAddOk) + " regUpdateOk " + str(regUpdateOk)
    mensaje += (
        " regCsvError " + str(regError) + " TotRegCsv " + str(regAddOk + regUpdateOk + regError)
    )

    masivo_file.observaciones = masivo_file.observaciones + mensaje
    masivo_file.save(update_fields=["estado", "observaciones"])
    return termina
