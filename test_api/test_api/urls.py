"""test_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
# from snippets import views
from operacion import views as views_operacion
from empleado import views as views_empleado
from clientes import views as views_clientes
from repartidores import views as views_repartidores
from proveedores import views as views_proveedores
from inventario import views as views_inventario
from municipio import views as views_municipios

router = DefaultRouter()
router.register(r'operacion', views_operacion.OperacionViewSet, basename='operacion')
router.register(r'flujo_operacion', views_operacion.FlujoViewSet, basename='flujo')
router.register(r'empleados', views_empleado.EmpleadoViewSet, basename='empleado')
router.register(r'clientes', views_clientes.ClienteViewSet, basename='cliente')
# router.register(r'repartidores', views_repartidores.RepartidorViewSet, basename='repartidor')
router.register(r'proveedores', views_proveedores.ProveedorViewSet, basename='proveedor')
router.register(r'inventario', views_inventario.InventarioViewSet, basename='inventario')
router.register(r'municipios', views_municipios.MunicipioViewSet, basename='municipio')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
