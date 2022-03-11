import os
import time
import django
import random as rd
from random import random
from django.contrib.auth.models import User

from cliente.models import cliente
from tareas.procesos.territorial_singleton import territorial_list

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "turing.settings")

django.setup()

vocals = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
consonants = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "x",
    "y",
    "z",
    "B",
    "C",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "X",
    "Y",
    "Z",
]


def generate_string(length: int) -> str:
    """Arma una cadena con caracteres aleatorios"""
    if length <= 0:
        return False
    # print(f"generate_string length {length}")

    character: str = ""
    for i in range(length):
        decision: str = ""
        decision = rd.choice(("vocals", "consonants"))
        if character[-1:].lower() in vocals:
            decision = "consonants"
        if character[-1:].lower() in consonants:
            decision = "vocals"
        if decision == "vocals":
            character += rd.choice(vocals)
        else:
            character += rd.choice(consonants)
    return character


def generate_number() -> int:
    number: int = 0
    number = int(random() * 20 + 1)
    # print(f"generate_number {number}")
    return number


def generate_city_id() -> int:
    """
    Se genera un entero entre 6 y 10 porque se crearon 5 ciudades
    """
    return rd.randint(6, 10)


def generate_category_id() -> int:
    """
    Se genera un entero entre 6 y 10 porque se crearon 5 ciudades
    """
    return rd.randint(1, 12)


def get_system_user_id():
    """Obtiene el id del usuarios del sistema"""
    user_qs = User.objects.filter(username__iexact="system_user")
    if user_qs.exists() and user_qs.count() != 0:
        user_qs = User.objects.get(username__iexact="system_user")
        return user_qs.id


def generate_cliente(count: int):
    user_id: int = 0
    user_id = get_system_user_id()
    for j in range(count):
        print(f"Generando cliente #{j} . . .")
        random_name: str = ""
        random_category_id: int = 0
        random_city_id: int = 0
        random_departament_id: int = 0
        random_country_id: int = 0
        random_name = generate_string(generate_number())
        random_category_id = generate_category_id()
        random_city_id = generate_city_id()
        # print (f"generate_cliente city_id = {str(random_city_id)}")
        random_departament_id = territorial_list.get_instance().get_city_parent_id(random_city_id)
        # print (f"generate_cliente departament_id = {str(random_departament_id)}")
        random_country_id = territorial_list.get_instance().get_departament_parent_id(
            random_departament_id
        )
        # print (f"generate_cliente random_country_id = {str(random_country_id)}")
        # parent_id = territorial_list.get_instance().get_country_parent_id(random_country_id)
        # print (f"generate_cliente parent_id = {str(parent_id)}")

        cliente.objects.create(
            name=random_name,
            user_created_id=user_id,
            category_id=random_category_id,
            country_id=random_country_id,
            departament_id=random_departament_id,
            city_id=random_city_id,
        )


if __name__ == "__main__":
    print("Inicio de creación de población")
    print("Por favor espere . . . ")
    start = time.strftime("%c")
    print(f"Fecha y hora de inicio: {start}")
    generate_cliente(190000)
    end = time.strftime("%c")
    print(f"Fecha y hora de finalización: {end}")
