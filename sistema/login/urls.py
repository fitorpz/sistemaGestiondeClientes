from django.urls import path
from . import views
from .views import detalles_modelo, procesar_formulario_cliente, cerrar_sesion, iniciar_sesion_cliente

urlpatterns = [
    path('', views.index, name='index'),
    path('procesar-formulario-cliente/', procesar_formulario_cliente, name='procesar_formulario_cliente'),
    path('detalles-modelo/<int:modelo_id>/', detalles_modelo, name='detalles_modelo'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('iniciar-sesion-cliente/', iniciar_sesion_cliente, name='iniciar_sesion_cliente'),

    # Define más URL según las vistas de tu aplicación
]