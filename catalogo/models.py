from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField("descripción")

    def __str__(self):
        return self.nombre


class LugarPatrimonial(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField("descripción")
    ubicacion = models.CharField("ubicación", max_length=150)
    anio_construccion = models.IntegerField("año de construcción")
    imagen = models.URLField("URL de la imagen", blank=True)
    # Cada lugar pertenece a una categoría. Una categoría tiene muchos lugares.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "lugares patrimoniales"

    def __str__(self):
        return self.nombre
