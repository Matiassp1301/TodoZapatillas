from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Tablas de la base de datos para el proyecto de productos 
# Create your models here.
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Orden {self.numero} - {self.usuario.username}"

class ProductoOrdenado(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} x{self.cantidad} (Orden: {self.orden.numero})"
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
    
class ProductoSQL(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15)         
    categoria = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    talla = models.CharField(max_length=10)
    precio = models.FloatField()
    proveedor = models.CharField(max_length=30)
    marca = models.CharField(max_length=100)
    valoracion = models.FloatField(null=True, blank=True)
    url_imagen = models.TextField()
    cantidad = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'productos'
        managed = False

