from django.contrib import admin
from .models import cliente
from .models import category
from .models import territorial
# Register your models here.

admin.site.register(cliente)
admin.site.register(category)
admin.site.register(territorial)
