from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views
from operacion import views as o_views
from empleado import views as empleado_views
from clientes import views as clientes_views
from repartidores import views as repartidores_views
from proveedores import views as proveedores_views
from inventario import views as inventario_views
from municipio import views as municipio_views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'operaciones', o_views.OperacionViewSet, basename='operacion')
router.register(r'empleados', empleado_views.EmpleadoViewSet, basename='empleado')
router.register(r'clientes', clientes_views.ClienteViewSet, basename='cliente')
router.register(r'repartidores', repartidores_views.RepartidorViewSet, basename='repartidor')
router.register(r'proveedores', proveedores_views.ProveedorViewSet, basename='proveedor')
router.register(r'inventario', inventario_views.InventarioViewSet, basename='inventario')
router.register(r'municipios', municipio_views.MunicipioViewSet, basename='municipio')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
