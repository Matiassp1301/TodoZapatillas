from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from .models import Producto
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType

def iniciar_pago(request):
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = 50000
    return_url = "http://127.0.0.1:8000/webpay-plus/commit"
    
    response = Transaction.create(buy_order, session_id, amount, return_url)
    
    return render(request, 'payment.html', {
        'response': response,
        'amount': amount
    })

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

def pago(request):
    return render(request, 'pago.html')

def exitoCompra(request):
    return render(request, 'exito.html')