from django.contrib import admin
from django.urls import path, include
from cliente.views import index_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cliente/", include(("cliente.urls", "cliente"))),
    path("", index_view, name="index"),
]
