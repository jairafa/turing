import datetime
import pytz
from datetime import *

from cliente.models import cliente
from processes.client_write_csv import UtilCsv

Vector = []


def client_excel(clients: Vector):
    print(f"cantidad de clientes: ({str(len(clients))})")
    utc = pytz.UTC
    fecha = datetime.now().replace(tzinfo=utc)
    file_name_csv: str = ""
    hoy: str = ""
    hoy = fecha.strftime("%Y%m%d_%H%M%S")
    # print(f"hoy {hoy} type {type(hoy)}")
    file_name_csv = "clientes-" + hoy + ".csv"
    csv = UtilCsv(file_name_csv)
    # print(f"Inicio ************************ Archivo de salida: {csv.get_name()}*************")

    for client in clients:
        line = {}
        line["id"] = client.id
        line["name"] = client.name
        line["departament"] = client.departament.name
        line["city"] = client.city.name
        line["category"] = client.category.name
        line["user_created"] = client.user_created.username
        line["created_at"] = client.created_at.strftime("%Y-%m-%d %H:%M")
        csv.write(line)
    csv.cerrar_csv()
    return (file_name_csv, csv.get_name())
