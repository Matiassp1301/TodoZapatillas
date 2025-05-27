from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def carrito(request):
    return render(request, 'carrito.html')

def detalle(request):
    return render(request, 'detalle.html')
