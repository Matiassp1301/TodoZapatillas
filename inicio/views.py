from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction as db_transaction
from django.db.models import Min, Avg, Max, Count
from django.utils import timezone
import json, random, uuid
from datetime import datetime

from .models import ProductoSQL, Orden, ProductoOrdenado

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType



def inicio(request):
    productos = (
        ProductoSQL.objects
        .values('nombre', 'categoria', 'marca')
        .annotate(
            id=Min('id'),
            precio=Min('precio'),
            url_imagen=Min('url_imagen'),
            proveedor=Min('proveedor'),
            valoracion=Avg('valoracion')
        )
        .order_by('nombre', 'categoria', 'marca')
    )
    categorias = ProductoSQL.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    return render(request, 'inicio.html', {'productos': productos, 'categorias': categorias})
# Create your views here.
@login_required(login_url=reverse_lazy('users:login'))
def carrito(request):
    categorias = ProductoSQL.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    return render(request, 'carrito.html', {'categorias': categorias})

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
    producto = get_object_or_404(ProductoSQL, id=producto_id)
    variantes = ProductoSQL.objects.filter(
        nombre=producto.nombre,
        marca=producto.marca,
        categoria=producto.categoria
    )
    colores = sorted(set(v.color for v in variantes))
    tallas = sorted(set(v.talla for v in variantes))
    proveedores = sorted(set(v.proveedor for v in variantes))
    precios = sorted(set(v.precio for v in variantes))
    cantidades = variantes.count()
    colores_css = [(color, color_css(color)) for color in colores]

    # Prepara las variantes como lista de diccionarios para JS
    variantes_json = json.dumps([
        {
            "proveedor": v.proveedor,
            "precio": v.precio,
            "color": v.color,
            "colorcss": color_css(v.color),
            "talla": v.talla
        }
        for v in variantes
    ])
    historial = request.session.get('historial_vistos', [])
    if producto.id not in historial:
        historial.append(producto.id)
        request.session['historial_vistos'] = historial

    categorias = ProductoSQL.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    return render(request, 'detalle.html', {
        'producto': producto,
        'colores': colores,
        'tallas': tallas,
        'proveedores': proveedores,
        'precios': precios,
        'colores_css': colores_css,
        'cantidades': cantidades,
        'variantes': variantes,
        'variantes_json': variantes_json,  # <-- ¡Esto es lo importante!
        'categorias': categorias,
        'usuario_logueado': request.user.is_authenticated
    })

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

def pago(request):
    return render(request, 'pago.html')



@login_required
def pago_exitoso(request):
    usuario = request.user
    try:
        orden = Orden.objects.filter(usuario=usuario).latest('fecha')
        productos = orden.productos.all()
    except Orden.DoesNotExist:
        orden = None
        productos = []

    contexto = {
        'orden': orden,
        'productos': productos,
    }
    return render(request, 'exito.html', contexto)

@login_required
@csrf_exempt
@login_required
@csrf_exempt
@csrf_exempt
def guardar_orden(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito', [])
            if not carrito:
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            total = 0
            for item in carrito:
                total += float(item['precio']) * int(item['cantidad'])

            with db_transaction.atomic():
                numero_orden = uuid.uuid4().hex[:10].upper()
                orden = Orden.objects.create(
                    usuario=request.user,
                    fecha=timezone.now(),
                    numero=numero_orden,
                    total=total
                )
                for item in carrito:
                    ProductoOrdenado.objects.create(
                        orden=orden,
                        nombre=item['nombre'],
                        cantidad=item['cantidad'],
                        precio=item['precio']
                    )
            return JsonResponse({
                'orden_numero': orden.numero,
                'monto': orden.total,
                'fecha': orden.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'mensaje': 'Orden guardada correctamente.'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def filtros(request):
    # Obtener filtros seleccionados
    categoria = request.GET.get('categoria', '')
    color = request.GET.get('color', '')
    talla = request.GET.get('talla', '')
    marca = request.GET.get('marca', '')
    proveedor = request.GET.get('proveedor', '')
    valor_min = request.GET.get('valor_min', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    tipo = request.GET.get('tipo', '')
    query = request.GET.get('query', '')

    # Base queryset con todos los filtros activos
    productos_qs = ProductoSQL.objects.all()
    if categoria:
        productos_qs = productos_qs.filter(categoria=categoria)
    if color:
        productos_qs = productos_qs.filter(color=color)
    if talla:
        productos_qs = productos_qs.filter(talla=talla)
    if marca:
        productos_qs = productos_qs.filter(marca=marca)
    if proveedor:
        productos_qs = productos_qs.filter(proveedor=proveedor)
    if tipo:
        productos_qs = productos_qs.filter(tipo=tipo)
    if valor_min:
        productos_qs = productos_qs.filter(valoracion__gte=valor_min)
    if precio_min:
        productos_qs = productos_qs.filter(precio__gte=precio_min)
    if precio_max:
        productos_qs = productos_qs.filter(precio__lte=precio_max)
    if query:
        productos_qs = productos_qs.filter(nombre__icontains=query)

    # Precio máximo disponible según los filtros activos
    precio_min_disponible = productos_qs.aggregate(minimo=Min('precio'))['minimo'] or 0
    precio_max_disponible = productos_qs.aggregate(maximo=Max('precio'))['maximo'] or 0

    # Colores disponibles y su cantidad (NO filtrar por color aquí)
    colores_qs = ProductoSQL.objects.all()
    if categoria:
        colores_qs = colores_qs.filter(categoria=categoria)
    if talla:
        colores_qs = colores_qs.filter(talla=talla)
    if marca:
        colores_qs = colores_qs.filter(marca=marca)
    if proveedor:
        colores_qs = colores_qs.filter(proveedor=proveedor)
    if valor_min:
        colores_qs = colores_qs.filter(valoracion__gte=valor_min)
    if precio_min:
        colores_qs = colores_qs.filter(precio__gte=precio_min)
    if precio_max:
        colores_qs = colores_qs.filter(precio__lte=precio_max)
    colores = colores_qs.exclude(color__isnull=True).exclude(color__exact='').values('color').annotate(count=Count('id')).order_by('color')
    
    # Tallas disponibles y su cantidad (NO filtrar por talla aquí)
    tallas_qs = ProductoSQL.objects.all()
    if categoria:
        tallas_qs = tallas_qs.filter(categoria=categoria)
    if color:
        tallas_qs = tallas_qs.filter(color=color)
    if marca:
        tallas_qs = tallas_qs.filter(marca=marca)
    if proveedor:
        tallas_qs = tallas_qs.filter(proveedor=proveedor)
    if valor_min:
        tallas_qs = tallas_qs.filter(valoracion__gte=valor_min)
    if precio_min:
        tallas_qs = tallas_qs.filter(precio__gte=precio_min)
    if precio_max:
        tallas_qs = tallas_qs.filter(precio__lte=precio_max)
    tallas = tallas_qs.exclude(talla__isnull=True).exclude(talla__exact='').values('talla').annotate(count=Count('id')).order_by('talla')
    
    # Marcas disponibles y su cantidad (NO filtrar por marca aquí)
    marcas_qs = ProductoSQL.objects.all()
    if categoria:
        marcas_qs = marcas_qs.filter(categoria=categoria)
    if color:
        marcas_qs = marcas_qs.filter(color=color)
    if talla:
        marcas_qs = marcas_qs.filter(talla=talla)
    if proveedor:
        marcas_qs = marcas_qs.filter(proveedor=proveedor)
    if valor_min:
        marcas_qs = marcas_qs.filter(valoracion__gte=valor_min)
    if precio_min:
        marcas_qs = marcas_qs.filter(precio__gte=precio_min)
    if precio_max:
        marcas_qs = marcas_qs.filter(precio__lte=precio_max)
    marcas = marcas_qs.exclude(marca__isnull=True).exclude(marca__exact='').values('marca').annotate(count=Count('id')).order_by('marca')
    
    # Proveedores disponibles y su cantidad (NO filtrar por proveedor aquí)
    proveedores_qs = ProductoSQL.objects.all()
    if categoria:
        proveedores_qs = proveedores_qs.filter(categoria=categoria)
    if color:
        proveedores_qs = proveedores_qs.filter(color=color)
    if talla:
        proveedores_qs = proveedores_qs.filter(talla=talla)
    if marca:
        proveedores_qs = proveedores_qs.filter(marca=marca)
    if valor_min:
        proveedores_qs = proveedores_qs.filter(valoracion__gte=valor_min)
    if precio_min:
        proveedores_qs = proveedores_qs.filter(precio__gte=precio_min)
    if precio_max:
        proveedores_qs = proveedores_qs.filter(precio__lte=precio_max)
    proveedores = proveedores_qs.exclude(proveedor__isnull=True).exclude(proveedor__exact='').values('proveedor').annotate(count=Count('id')).order_by('proveedor')
    # Productos filtrados finales
    productos = (
        productos_qs
        .values('nombre', 'categoria', 'marca')
        .annotate(
            id=Min('id'),
            precio=Min('precio'),
            url_imagen=Min('url_imagen'),
            proveedor=Min('proveedor'),
            valoracion=Avg('valoracion')
        )
        .order_by('nombre', 'categoria', 'marca')
    )

    categorias = ProductoSQL.objects.values_list('categoria', flat=True).distinct().order_by('categoria')

    return render(request, 'filtros.html', {
        'productos': productos,
        'categorias': categorias,
        'colores': colores,
        'tallas': tallas,
        'marcas': marcas,
        'proveedores': proveedores,
        'categoria_sel': categoria,
        'color_sel': color,
        'talla_sel': talla,
        'marca_sel': marca,
        'proveedor_sel': proveedor,
        'valor_min': valor_min,
        'precio_min_disponible': precio_min_disponible,
        'precio_max_disponible': precio_max_disponible,
        'tipo_sel': tipo,
        'query': query,
    })

def perfil_usuario(request):
    return render(request, 'perfil_usuario.html', {
        'usuario': request.user
    })


@login_required
def historial_vistos(request):
    ids = request.session.get('historial_vistos', [])
    from django.db.models import Case, When
    orden_preservado = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(ids)])
    productos = ProductoSQL.objects.filter(id__in=ids).order_by(orden_preservado)
    return render(request, 'vistos.html', {'productos': productos})

def historial_pagos(request):
    usuario = request.user
    ordenes = Orden.objects.filter(usuario=usuario).order_by('-fecha')

    # Recolectar todos los productos por orden
    compras = []
    for orden in ordenes:
        for producto in orden.productos.all():
            compras.append({
                'producto': producto.nombre,
                'cantidad': producto.cantidad,
                'total': producto.precio * producto.cantidad,
                'fecha': orden.fecha,
                'estado': 'Pagado',  # puedes agregar un campo real si lo tienes
            })

    return render(request, 'historial_pagos.html', {'compras': compras})



    if request.method == 'POST':
        try:
            # Leer carrito desde JSON recibido en POST
            data = json.loads(request.body)
            carrito = data.get('carrito', [])

            if not carrito:
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            with db_transaction.atomic():
                # Generar número único para la orden (10 caracteres hexadecimales)
                numero_orden = uuid.uuid4().hex[:10].upper()

                # Calcular total sumando precio*cantidad de cada producto
                total = sum(item['precio'] * item['cantidad'] for item in carrito)

                # Crear la orden
                orden = Orden.objects.create(
                    usuario=request.user,
                    fecha=timezone.now(),
                    numero=numero_orden,
                    total=total
                )

                # Guardar productos ordenados relacionados a la orden
                for item in carrito:
                    ProductoOrdenado.objects.create(
                        orden=orden,
                        producto_id=item['producto_id'],  # asumiendo campo FK a ProductoSQL o similar
                        cantidad=item['cantidad'],
                        precio=item['precio']
                    )

            # Retornar datos de la orden para confirmar éxito
            return JsonResponse({
                'orden_numero': orden.numero,
                'monto': orden.total,
                'fecha': orden.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'mensaje': 'Orden guardada correctamente.'
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)