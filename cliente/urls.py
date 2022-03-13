from django.urls import path

from cliente.views import (
    client_create,
    client_delete,
    client_edit,
    client_filter_view,
    client_list,
    client_list_view,
    client_update,
    territorial_get_sons,
)

s_url_list: str = "list_class/<str:s_order>/<int:id>/<int:city_id>/<int:departament_id>/"
s_url_list += "<int:category_id>/<str:name>/<str:fecha_ini>/<str:fecha_fin>"
urlpatterns = [
    path("find/", client_filter_view, name="client_filter"),
    path("edit/<int:pk>/", client_edit.as_view(), name="client_edit"),
    path("update/<int:pk>/", client_update.as_view(), name="client_update"),
    path("delete/<int:pk>/", client_delete.as_view(), name="client_delete"),
    path("create/", client_create.as_view(), name="client_add"),
    # path("list/<str:page_obj>", client_list.as_view(), name="client_list"),
    path("list_func/", client_list_view, name="client_list_view"),
    path("list/<str:s_order>", client_list.as_view(), name="client_list_class"),
    path(
        s_url_list,
        client_list.as_view(),
        name="client_list_class",
    ),
    path("territorial_get_sons/", territorial_get_sons, name="ajax_territorial_get_sons"),
]
