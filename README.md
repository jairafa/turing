## Prueba Técnica - AITuring
> Aplicacion CRUD en djando para gestionar clientes
# Funcionalidades
## 1. Migración de datos
Al realizar la migración se poblan automaticamente las siguientes tablas:
- Categorias
Por medio de archivo plano ubicado en la siguiente ruta:
\turing\cliente\migrations\categorias.csv
- Territorios
Por medio de archivo plano ubicado en la siguiente ruta:
\turing\cliente\migrations\municipios.csv
- Clientes
Se carga automaticamente, los valores del nombre del cliente, territorios y categorías se generan aleatoriamente.
Para modificar la cantidad de clientes a insertar en la funcion generate_cliente ingresa el valor
\turing\processes\cliente_dummy.py
generate_cliente(190000)

## 2. Búsqueda de Clientes
Se tiene una pagina para aplicar diferentes filtros de busqueda de clientes
Para ingresar, seleccione la opción filtros clientes.
### 2.1 Filtros por:
> No Cliente, Nombre, fecha inicio y fin de creación de clientes, territorios.
> Se puede seleccionar el modo de ordenamiento, por identificador del  cliente: Asencente/Descendente
### 2.2 Informe de clientes
Presenta los datos asociados al cliente
- Permite la opción de presentar los datos de las siguiente formas:
> Generar un xls
> Ver los datos por pantalla
## 3. Administrador de Clientes
- El administrador de clientes permite realizar las siguientes operaciones:
> Consultar
> Actualizar
> Crear
> Eliminar (La eliminación es lógica)
- Ingreso al administrador de clientes
> Desde el menú principal, opción:
> - Filtros Clientes
> - Lista Clientes
## 4. Cargue masivo de clientes
La opción permite crear clientes ó modificar sus datos a partir de un archivo plano.
> La opción carga los clientes con un bulk create / update
- La busqueda se realiza por nombre de cliente
- Si encuentra el nombre del cliente, permite modificar el territorio y la categoría
- Si no encuentra el cliente, lo crea.
## 5. Idioma
La aplicación esta disponible para los siguientes Idiomas:
- Español
- Inglés

# Versionamiento

- Fecha Implenetación: 15/03/2022
- La aplicación se implemento en la siguiente versión

* Python 3.10.2
* Django 4.0.3
* Base de datos: sqlite
> Aunque en el repositorio se encuentra una base de datos funcional, la puede borrar y crear las migraciones que poblaran nuevamente la base de datos.
> turing\db.sqlite3

# Instalación
- Instale python
- Abra una terminal
- Cree una carpeta para el proyecto
- Descargue en la carpeta el proyecto desde github, ya sea desde un archivo zip (descomprímirlo) o por github
https://github.com/jairafa/turing.git
- Cree un entorno virtual y activelo
- Ubiquese en la carpeta raiz del proyecto, en ésta debe encontrar el archivo manage.py
turing\manage.py
- Instale los componentes
> pip install -r requirements.txt

# Ejecución
- Servidor
Estando en la terminal en la ruta principal del proyecto, ejecute:
turing\manage.py runserver
- Cliente web
Desde el browser:
http://localhost:8000/
