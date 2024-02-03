# urls.py dentro de la carpeta de tu aplicación

from django.urls import path
from . import views
from .views import agregar_registro, editar_registro, obtener_detalle_registro, actualizar_registro, eliminar_registro

urlpatterns = [
    path('', views.index, name='panelAdmin'),
    path('agregar_registro/', agregar_registro, name='agregar_registro/'),
    path('editar_registro/<int:id_registro>/', editar_registro, name='editar_registro/'),
    path('panelAdmin/obtener_detalle_registro', views.obtener_detalle_registro, name='obtener_detalle_registro'),
    path('actualizar_registro/', actualizar_registro, name='actualizar_registro/'),
    path('eliminar/<int:id_registro>/', eliminar_registro, name='eliminar_registro'),
    # Agrega más rutas según sea necesario
]
