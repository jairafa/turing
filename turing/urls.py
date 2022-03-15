from django.contrib import admin
from django.urls import path, include
from cliente.views import index_view

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("cliente/", include(("cliente.urls", "cliente"))),
    path("tareas/", include(("tareas.urls", "tareas"))),
    path("", index_view, name="index"),
]
