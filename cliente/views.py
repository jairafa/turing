import datetime

from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView

# from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect  # noqa: F811
from django.core.paginator import Paginator
from cliente.forms import client_form, client_filter_form, client_desable_form
from cliente.models import cliente, territorial
from functions.dates import convert_str_to_datetime, convert_date_to_datetime
from processes.client_excel import client_excel
from processes.download_file_csv import download_file

Vector = []
Dictionary = {}


def index_view(request):
    return render(request, "base/index.html")


def client_filter_view(request):
    elError = False
    form = client_filter_form(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        cliente_id: int = 0
        cliente_id = data["cliente_id"]
        name: str = ""
        name = data["name"]
        city = data["city"]
        departament = data["departament"]
        category = data["category"]
        fecha_ini = data["fecha_ini"]
        fecha_fin = data["fecha_fin"]
        order_by_id = data["order_by_id"]
        generar_xls = data["generar_xls"]

        if cliente_id:
            cliente_id = cliente_id
        else:
            cliente_id = 0
        if not name:
            name = "0"
        if city:
            city_id = city.id
        else:
            city_id = 0
        if departament:
            departament_id = departament.id
        else:
            departament_id = 0
        if category:
            category_id = category.id
        else:
            category_id = 0
        if not fecha_ini:
            fecha_ini = "0"
        if not fecha_fin:
            fecha_fin = "0"
        if not generar_xls:
            generar_xls = "N"

        if "S" in generar_xls:
            kwargs = {}
            kwargs["s_order"] = order_by_id
            kwargs["id"] = cliente_id
            kwargs["city_id"] = city_id
            kwargs["departament_id"] = departament_id
            kwargs["category_id"] = category_id
            kwargs["name"] = name
            kwargs["fecha_ini"] = fecha_ini
            kwargs["fecha_fin"] = fecha_fin
            clients: [cliente]
            clients = get_filtered_clients(kwargs)

            if len(clients) > 0:
                file_name: str = ""
                s_path_file: str = ""
                (file_name, s_path_file) = client_excel(clients)
                response = download_file(file_name, s_path_file)
                return response
            elError = "No existen clientes para el filtro indicado"
        else:
            return redirect(
                "cliente:client_list_class",
                s_order=order_by_id,
                id=cliente_id,
                city_id=city_id,
                departament_id=departament_id,
                category_id=category_id,
                name=name,
                fecha_ini=fecha_ini,
                fecha_fin=fecha_fin,
            )
    return render(
        request,
        "cliente/clients_find.html",
        {"form": form, "title": "Búsqueda de Clientes", "error": elError},
    )


def get_filtered_clients(kwargs: Dictionary) -> Vector:
    s_order: str = "asc"
    kwargs_filter = {}
    kwargs_filter["is_active"] = 1
    if "s_order" in kwargs:
        s_order = kwargs["s_order"]
    if "id" in kwargs:
        if kwargs["id"] != 0:
            kwargs_filter["id"] = kwargs["id"]
    if "city_id" in kwargs:
        if kwargs["city_id"] != 0:
            kwargs_filter["city_id"] = kwargs["city_id"]
    if "departament_id" in kwargs:
        if kwargs["departament_id"] != 0:
            kwargs_filter["departament_id"] = kwargs["departament_id"]
    if "category_id" in kwargs:
        if kwargs["category_id"] != 0:
            kwargs_filter["category_id"] = kwargs["category_id"]
    name: str = ""
    if "name" in kwargs:
        if kwargs["name"] != "0":
            name = kwargs["name"]
    s_fecha_ini: str = ""
    datetime_ini: datetime = None
    # print(f"datetime_ini antes {datetime_ini}")
    if "fecha_ini" in kwargs:
        if kwargs["fecha_ini"] != "0":
            s_fecha_ini = kwargs["fecha_ini"]
            # print(f"s_fecha_ini antes {s_fecha_ini}")
            # print(f"s_fecha_ini type {type(s_fecha_ini)}")
            if isinstance(s_fecha_ini, str):
                # print("Entra por str")
                datetime_ini = convert_str_to_datetime(s_fecha_ini, "initial")
            else:
                # print("Entra por date")
                datetime_ini = convert_date_to_datetime(s_fecha_ini, "initial")
            # print(f"datetime_ini despues {datetime_ini}")
            # print(f"datetime_ini type {type(datetime_ini)}")
    s_fecha_fin: str = ""
    datetime_fin: datetime = None
    # print(f"datetime_fin antes {datetime_fin}")
    if "fecha_fin" in kwargs:
        if kwargs["fecha_fin"] != "0":
            s_fecha_fin = kwargs["fecha_fin"]
            # print(f"s_fecha_fin antes {s_fecha_fin}")
            # datetime_fin = convert_str_to_datetime(s_fecha_fin, "final")
            if isinstance(s_fecha_fin, str):
                datetime_fin = convert_str_to_datetime(s_fecha_fin, "final")
            else:
                datetime_fin = convert_date_to_datetime(s_fecha_fin, "final")
            # print(f"datetime_fin despues {datetime_fin}")
            # print(f"datetime_fin type {type(datetime_fin)}")

    s_order_by_is: str = "-id"
    if s_order == "asc":
        s_order_by_is = "id"

    if len(name) > 0:
        if datetime_ini and datetime_fin:
            clients = (
                cliente.objects.filter(**kwargs_filter)
                .filter(name__icontains=name)
                .order_by(s_order_by_is)[:1000]
            )
        else:
            clients = (
                cliente.objects.filter(**kwargs_filter)
                .filter(name__icontains=name)
                .filter(created_at__range=(datetime_ini, datetime_fin))
                .order_by(s_order_by_is)[:1000]
            )
    else:
        if datetime_ini and datetime_fin:
            clients = (
                cliente.objects.filter(**kwargs_filter)
                .filter(created_at__range=(datetime_ini, datetime_fin))
                .order_by(s_order_by_is)[:1000]
            )
        else:
            clients = cliente.objects.filter(**kwargs_filter).order_by(s_order_by_is)[:1000]
    return clients


class client_list(ListView):
    template_name = "cliente/clients_list.html"
    model = cliente
    ordering = "-id"
    paginate_by = 10
    context_object_name = "clients"

    def get_context_data(self, **kwargs):
        context = super(client_list, self).get_context_data(**kwargs)
        context["title"] = "Selección de Clientes"
        return context

    def get_queryset(self):
        clients: Vector
        clients = get_filtered_clients(self.kwargs)
        return clients


def client_list_view(request):
    """
    clients = contexto['clients']
    paginator = Paginator(clients, 10)
    page_obj = request.GET.get('page_obj')
    clients = paginator.get_page(page_obj)
    contexto = {"page_obj": clients, "title": "Lista de Clientes"}
    """
    return render(request, "cliente/clients_list.html")


class client_edit(TemplateView):
    template_name = "cliente/clients_detail.html"

    def get_context_data(self, *args, **kwargs):
        # El pk que pasas a la URL
        pk = self.kwargs.get("pk")
        context = super(client_edit, self).get_context_data(**kwargs)
        context["cliente"] = cliente.objects.get(id=pk)
        context["title"] = "Detalle Cliente"
        return context


class client_create(CreateView):
    model = cliente
    template_name = "Cliente/clients_changes.html"
    form_class = client_form

    def get_context_data(self, **kwargs):
        context = super(client_create, self).get_context_data(**kwargs)
        context["title"] = "Creación de Clientes"
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render(self.get_context_data(form=form))
        """
        msg = 'UsuariosCargoLocalidad (' + form.errors.as_text() + ')'
        msg = msg.replace('*','')
        msg = msg.replace('__all__','')
        return render(self.request, 'elError.html', {'errors':msg})
        """

    def form_valid(self, request, form):
        # elRadicado = crear.cleaned_data
        # user = auth.get_user(self.request)

        # data = form.cleaned_data
        # print(cubrimiento)
        form.save()
        # frmRad = form.save(commit = False) #solicitar2Form.cleaned_data
        # frmRad.save()
        # return redirect("cliente:client_filter", user_correo_id =data['user_correo'].id)
        return redirect("cliente:client_list_class", s_order="desc")


class client_update(UpdateView):
    model = cliente
    form_class = client_form
    template_name = "cliente/clients_changes.html"

    def get_context_data(self, **kwargs):
        context = super(client_update, self).get_context_data(**kwargs)
        context["title"] = "Actualizar Cliente"
        pk = self.kwargs.get("pk", 0)
        cliente = self.model.objects.get(id=pk)
        context["form"] = self.form_class(instance=cliente)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render(self.get_context_data(form=form))

    def form_valid(self, request, form):
        form.save()
        return redirect("cliente:client_list_class", s_order="desc")


class client_delete(UpdateView):
    model = cliente
    template_name = "cliente/clients_changes.html"
    form_class = client_desable_form

    def get_context_data(self, **kwargs):
        context = super(client_delete, self).get_context_data(**kwargs)
        context["title"] = "Eliminar Cliente"
        pk = self.kwargs.get("pk", 0)
        cliente = self.model.objects.get(id=pk)
        context["form"] = self.form_class(instance=cliente)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render(self.get_context_data(form=form))

    def form_valid(self, request, form):
        client = form.save(commit=False)
        client.is_active = 0
        client.save()
        return redirect("cliente:client_list_class", s_order="desc")


def territorial_get_sons(request):
    """Obtiene todos los hijos de un territorio padre"""
    s_parent_id: str = ""
    if request.method == "POST":
        s_parent_id = request.POST.get("ajax_parent_id")
    else:
        s_parent_id = request.GET.get("ajax_parent_id")
    # print(f"ajax territorial_get_sons s_parent_id: {s_parent_id}")

    territorials = []
    territorials = territorial.objects.filter(parent_id=s_parent_id).order_by("name")
    return render(request, "base/dropdown_list_options.html", {"options": territorials})
