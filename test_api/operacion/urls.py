from django.urls import path, include
from rest_framework.routers import DefaultRouter

from operacion import views
#
# router = DefaultRouter()
# router.register(r'operaciones', views.OperacionViewSet, basename='operaciones')
#
# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]
