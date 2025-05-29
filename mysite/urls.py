"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# Importar las vistas de las paginas
from inicio.views import inicio, carrito, detalle
urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Path Inicio (Catalogo)
    path('', include('inicio.urls')), # app inicio, vista inicio (catalogo de productos)

    # Path Soporte

    # Path Carrito de compra
    path("cart/", carrito), # app inicio, vista carrito
    # Path Perfil de usuario

    # Path Detalle de producto
    path('detalle/<int:producto_id>/', detalle, name='detalle'),
    # 
    
]
