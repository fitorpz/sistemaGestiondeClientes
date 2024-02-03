from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from panelAdmin.models import panelAdmin
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse


# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def detalles_modelo(request, modelo_id):
    # Obtener el objeto modelo desde la base de datos
    modelo = get_object_or_404(panelAdmin, id=modelo_id)

    # Renderizar la plantilla y pasar el objeto modelo como contexto
    return render(request, 'login/datoscliente.html', {'modelo': modelo})

def procesar_formulario_cliente(request):
    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'iniciar_sesion_cliente':
            # Manejar la acción de inicio de sesión como cliente
            # ... tu lógica aquí ...
            try:
                # Obtén los datos del cliente desde la base de datos (ajusta esto según tus necesidades)
                datos_cliente = panelAdmin.objects.get(cuenta=request.POST.get('cuenta'))

                # Añade los campos calculados a los datos del cliente
                hoy = datetime.now().date()

                # Calcula fechaVencimiento y diasServicio
                if datos_cliente.fechaUltimoPago and datos_cliente.plan:
                    # Convierte datos_cliente.fechaUltimoPago a datetime si es de tipo date
                    if isinstance(datos_cliente.fechaUltimoPago, datetime):
                        datos_cliente.fechaUltimoPago = datetime.combine(datos_cliente.fechaUltimoPago, datetime.min.time())

                    # Convierte hoy a datetime para que ambos objetos sean del mismo tipo
                    hoy = datetime.combine(hoy, datetime.min.time())

                    # Calcula la fecha de vencimiento
                    if datos_cliente.plan == 'mensual':
                        fecha_vencimiento = datos_cliente.fechaUltimoPago + timedelta(days=31)
                    elif datos_cliente.plan == 'trimestral':
                        fecha_vencimiento = datos_cliente.fechaUltimoPago + timedelta(days=91)
                    elif datos_cliente.plan == 'semestral':
                        fecha_vencimiento = datos_cliente.fechaUltimoPago + timedelta(days=211)
                    elif datos_cliente.plan == 'anual':
                        fecha_vencimiento = datos_cliente.fechaUltimoPago + timedelta(days=425)
                    else:
                        # En caso de que el plan no sea reconocido, establece una fecha de vencimiento predeterminada
                        fecha_vencimiento = datos_cliente.fechaUltimoPago + timedelta(days=30)

                    # Calcula los días de servicio restantes
                    dias_servicio_restantes = (fecha_vencimiento - hoy).days

                    # Asigna los valores calculados al objeto panelAdmin
                    datos_cliente.fechaVencimiento = fecha_vencimiento
                    datos_cliente.diasServicio = dias_servicio_restantes if dias_servicio_restantes >= 0 else 0

                # Redirigir o mostrar la respuesta adecuada
                return render(request, 'login/datoscliente.html', {'cliente': datos_cliente})

            except panelAdmin.DoesNotExist:
                return render(request, 'login/datoscliente.html', {'mensaje': 'Cliente no encontrado'})

    # Si no es una solicitud POST o no hay acción definida, puedes redirigir a una página de error o manejarlo de otra manera
    return HttpResponseBadRequest("Solicitud no válida")


def cerrar_sesion(request):
    logout(request)
    return JsonResponse({'mensaje': 'Sesión cerrada correctamente'})

def iniciar_sesion_cliente(request):
    if request.method == 'POST':
        cuenta = request.POST.get('cuenta')
        contrasena = request.POST.get('contrasena')

        usuario = authenticate(request, username=cuenta, password=contrasena)

        if usuario is not None:
            login(request, usuario)
            return redirect('panelAdmin')  # Ajusta según tu configuración de URLs
        else:
            return HttpResponse('Autenticación fallida')

    return render(request, 'panelAdmin.html')  # Ajusta según tu configuración de templates

