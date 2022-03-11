from django.db import models
from django.contrib.auth.models import User


class category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "{} ".format(self.name)


class territorial(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self", models.DO_NOTHING, related_name="dad", blank=True, null=True
    )
    territorial_list = (
        (
            "P",
            "Pais",
        ),
        (
            "D",
            "Departamento",
        ),
        (
            "C",
            "Ciudad",
        ),
    )  # noqa
    territorial_type = models.CharField(
        "Tipo Territorio", max_length=12, choices=territorial_list, default="city"
    )
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "{} {} {} padre {}".format(
            self.id, self.name, self.territorial_type, self.parent_id
        )


class cliente(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(
        territorial, models.DO_NOTHING, related_name="pais", blank=False, null=False
    )
    departamen = models.ForeignKey(
        territorial,
        models.DO_NOTHING,
        related_name="departamento",
        blank=False,
        null=False,
    )
    city = models.ForeignKey(
        territorial, models.DO_NOTHING, related_name="ciudad", blank=False, null=False
    )
    category = models.ForeignKey(category, models.DO_NOTHING, blank=False, null=False)
    user_created = models.ForeignKey(User, models.DO_NOTHING)
    active = (
        (
            1,
            "activo",
        ),
        (
            0,
            "inactivo",
        ),
    )
    is_active = models.PositiveSmallIntegerField(choices=active, default=1)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "{} {} {}".format(self.id, self.name, self.city)
