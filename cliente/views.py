from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView

# from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect  # noqa: F811
from cliente.forms import client_form, client_filter_form
from cliente.models import cliente


def index_view(request):
    count = User.objects.count()
    return render(request, "base/index.html", {"count": count})


def client_filter_view(request):
    elError = False
    form = client_filter_form(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        cliente_id = data["cliente_id"]
        name = data["name"]
        city = data["city"]
        departament = data["departament"]
        category = data["category"]

        kwargs = {}
        if cliente_id:
            kwargs["id"] = cliente_id
        if name:
            kwargs["name"] = name
        if city:
            kwargs["city_id"] = city.id
        if departament:
            kwargs["departament_id"] = departament.id
        if category:
            kwargs["category_id"] = category.id

        if len(kwargs) != 0:
            clients = cliente.objects.filter(**kwargs).order_by("-name")[:1000]
            contexto = {"clients": clients, "title": "Lista de Clientes"}
            return render(request, "cliente/clients_list.html", contexto)
        else:
            elError = True
    return render(
        request,
        "cliente/clients_find.html",
        {"form": form, "title": "Búsqueda de Clientes", "error": elError},
    )


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


class client_list(ListView):
    template_name = "cliente/clientes_list.html"
    model = cliente
    ordering = "-id"
    paginate_by = 20
    context_object_name = "clientes"

    def get_queryset(self):
        # pk = self.kwargs["pk"]
        return cliente.objects.filter(**self.kwargs).order_by("-id")
