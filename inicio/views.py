from django.shortcuts import render
from django.http import HttpResponse 
from .models import Producto

from .models import Producto

def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})
# Create your views here.
def carrito(request):
    return render(request, 'carrito.html')

def detalle(request):
    return render(request, 'detalle.html')
