from cliente.models import territorial


class territorial_list:
    """Clase para cargar en memoria los territorios para evitar accesos a la base de datos"""

    __instance = None
    Vector = []

    def __str__(self):
        return "territorial_list Singleton "

    def __new__(cls):
        if not territorial_list.__instance:
            territorial_list.__instance = object.__new__(cls)
        return territorial_list.__instance

    @staticmethod
    def get_instance():
        if not territorial_list.__instance:
            territorial_list.__instance = territorial_list()
        return territorial_list.__instance

    def seleccionar_elementos(self, sType: str) -> Vector:
        """Permite armar listas por cada tipo de territorio"""
        print(f"seleccionar_elementos sType {sType}")
        terr_list = (
            territorial.objects.filter(territorial_type=sType)
            .values("id", "parent_id")
            .order_by("id")
        )
        list = []

        for res in terr_list:
            print(f"seleccionar_elementos res {res}")
            list.append(res)

        return list

    def __init__(self):
        # print (f"territorial_list init " + "a" * 10)
        self.l_country = []
        self.l_country = self.seleccionar_elementos("P")
        # print (f"territorial_list init " + "b" * 10)
        self.l_departament = []
        self.l_departament = self.seleccionar_elementos("D")
        self.l_city = []
        self.l_city = self.seleccionar_elementos("C")
        # print (f"territorial_list init " + "c" * 10)

    def get_parent_id(self, id: int, sType: str, l_territory: Vector) -> int:
        """Busca el padre del territorio solicitado por parametro"""
        # print (f"get_parent_id id = {str(id)} sType {sType}")
        for elementos_lista in l_territory:
            # print(elementos_lista)
            # print (f"get_parent_id id = {str(id)} |
            # parent_id = {str(elementos_lista['parent_id'])} sType {sType}")
            if elementos_lista["id"] == id:
                # print (f"get_parent_id * return *
                # parent_id {str(elementos_lista['parent_id'])} sType {sType}")
                return elementos_lista["parent_id"]
        # print (f"get_parent_id return 0 sType {sType}")
        return 0

    def get_country_parent_id(self, id: int) -> int:
        """Obtiene el padre id del pais"""
        parent_id: int = 0
        parent_id = self.get_parent_id(id, "P", self.l_country)
        return parent_id

    def get_departament_parent_id(self, id: int) -> int:
        """Obtiene el pais id del departamento"""
        parent_id: int = 0
        parent_id = self.get_parent_id(id, "D", self.l_departament)
        return parent_id

    def get_city_parent_id(self, id: int) -> int:
        """Obtiene el departamento id de la ciudad"""
        parent_id: int = 0
        parent_id = self.get_parent_id(id, "C", self.l_city)
        return parent_id
