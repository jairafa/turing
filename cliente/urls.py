from django.urls import path

from cliente.views import (
    client_edit,
    client_create,
    client_list,
    client_list_view,
    client_filter_view,
)

urlpatterns = [
    path("find/", client_filter_view, name="client_filter"),
    path("edit/<int:pk>/", client_edit.as_view(), name="client_edit"),
    path("create/", client_create.as_view(), name="client_add"),
    # path("list/<str:page_obj>", client_list.as_view(), name="client_list"),
    path("list_func/", client_list_view, name="client_list_view"),
    path("list_all/", client_list.as_view(), name="client_list_class"),
    path(
        "list_class/<int:id>/<int:city_id>/<int:departament_id>/<int:category_id>/<str:name>",
        client_list.as_view(),
        name="client_list_class",
    ),
]
