from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from .models import Producto

def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})
# Create your views here.
def carrito(request):
    return render(request, 'carrito.html')

def color_css(nombre):
    mapa = {
        'negro': 'black',
        'blanco': 'white',
        'rojo': 'red',
        'rosa': 'pink',
        'gris': 'gray',
        'azul': 'blue',
        'verde': 'green',
        'amarillo': 'yellow',
        'café': 'saddlebrown',
        'marrón': 'brown',
        'beige': 'beige',
        'celeste': 'skyblue',
        'lila': 'plum',
        'morado': 'purple',
        'naranja': 'orange',
        'fucsia': 'fuchsia',
        'turquesa': 'turquoise',
        'dorado': 'gold',
        'plateado': 'silver',
        'vino': 'darkred',
        'oliva': 'olive',
    }
    return mapa.get(nombre.strip().lower(), nombre.strip().lower())

def detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    tallas = producto.tallas_disponibles if producto.tallas_disponibles else []
    colores = [c.strip() for c in (producto.color or "").split(",") if c.strip()]
    colores_css = [(color, color_css(color)) for color in colores]
    return render(request, 'detalle.html', {
        'producto': producto,
        'tallas': tallas,
        'colores_css': colores_css
    })
