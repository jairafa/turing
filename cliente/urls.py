from django.urls import path

from cliente.views import client_edit, client_create, client_list, client_filter_view

urlpatterns = [
    path("find/", client_filter_view, name="client_filter"),
    path("edit/<int:pk>/", client_edit.as_view(), name="client_edit"),
    path("create/", client_create.as_view(), name="client_add"),
    path("list/", client_list.as_view(), name="client_listar"),
]
