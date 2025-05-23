from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    precio = models.FloatField()
    tallas_disponibles = models.JSONField(default=list)  # lista de floats
    url_imagen = models.URLField(max_length=300, blank=True, null=True)
    proveedor = models.CharField(max_length=100)
    valoracion = models.FloatField(blank=True, null=True)
    comentario = models.JSONField(default=list, blank=True, null=True)  # lista de strings

    def __str__(self):
        return self.nombre