from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView

# from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect  # noqa: F811
from django.core.paginator import Paginator
from cliente.forms import client_form, client_filter_form
from cliente.models import cliente


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
        return redirect(
            "cliente:client_list_class",
            id=cliente_id,
            city_id=city_id,
            departament_id=departament_id,
            category_id=category_id,
            name=name,
        )
    return render(
        request,
        "cliente/clients_find.html",
        {"form": form, "title": "Búsqueda de Clientes", "error": elError},
    )


class client_list(ListView):
    template_name = "cliente/clients_list.html"
    model = cliente
    ordering = "-id"
    paginate_by = 10
    context_object_name = "clients"

    def get_queryset(self):

        kwargs_filter = {}

        if "id" in self.kwargs:
            if self.kwargs["id"] != 0:
                kwargs_filter["id"] = self.kwargs["id"]
        if "city_id" in self.kwargs:
            if self.kwargs["city_id"] != 0:
                kwargs_filter["city_id"] = self.kwargs["city_id"]
        if "departament_id" in self.kwargs:
            if self.kwargs["departament_id"] != 0:
                kwargs_filter["departament_id"] = self.kwargs["departament_id"]
        if "category_id" in self.kwargs:
            if self.kwargs["category_id"] != 0:
                kwargs_filter["category_id"] = self.kwargs["category_id"]

        name: str = ""
        if "name" in self.kwargs:
            if self.kwargs["name"] != "0":
                name = self.kwargs["name"]

        kwargs_filter["is_active"] = 1

        if len(name) > 0:
            clients = (
                cliente.objects.filter(**kwargs_filter)
                .filter(name__icontains=name)
                .order_by("id")[:1000]
            )
        else:
            clients = cliente.objects.filter(**kwargs_filter).order_by("id")[:1000]

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
        return redirect("cliente:client_filter")


class client_update(UpdateView):
    model = cliente
    template_name = "cliente/clients_changes.html"
    form_class = client_form

    def get_context_data(self, **kwargs):
        context = super(client_update, self).get_context_data(**kwargs)
        context["title"] = "Actualizar Cliente"
        return context


class client_delete(UpdateView):
    model = cliente
    template_name = "cliente/clients_changes.html"
    form_class = client_form

    def get_context_data(self, **kwargs):
        context = super(client_update, self).get_context_data(**kwargs)
        context["title"] = "Actualizar Cliente"
        return context
