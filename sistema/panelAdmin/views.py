from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from panelAdmin.models import panelAdmin
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from django.contrib import messages

def index(request):
    datos = panelAdmin.objects.all()

    hoy = datetime.now().date()

    for dato in datos:
        if dato.fechaUltimoPago and dato.plan:
            # Convierte dato.fechaUltimoPago a datetime si es de tipo date
            if isinstance(dato.fechaUltimoPago, datetime):
                dato.fechaUltimoPago = datetime.combine(dato.fechaUltimoPago, datetime.min.time())

            # Convierte hoy a datetime para que ambos objetos sean del mismo tipo
            hoy = datetime.combine(hoy, datetime.min.time())

            # Calcula la fecha de vencimiento
            if dato.plan == 'mensual':
                fecha_vencimiento = dato.fechaUltimoPago + timedelta(days=31)
            elif dato.plan == 'trimestral':
                fecha_vencimiento = dato.fechaUltimoPago + timedelta(days=91)
            elif dato.plan == 'semestral':
                fecha_vencimiento = dato.fechaUltimoPago + timedelta(days=211)
            elif dato.plan == 'anual':
                fecha_vencimiento = dato.fechaUltimoPago + timedelta(days=425)
            else:
                # En caso de que el plan no sea reconocido, establece una fecha de vencimiento predeterminada
                fecha_vencimiento = dato.fechaUltimoPago + timedelta(days=30)

            # Calcula los días de servicio restantes
            dias_servicio_restantes = (fecha_vencimiento - hoy).days

            # Asigna los valores calculados al objeto panelAdmin
            dato.fechaVencimiento = fecha_vencimiento
            dato.diasServicio = dias_servicio_restantes if dias_servicio_restantes >= 0 else 0

    # Pasa los datos actualizados a la plantilla
    context = {'datos': datos}
    return render(request, 'panelAdmin/panelAdmin.html', context)

def agregar_registro(request):
    if request.method == 'POST':
        cuenta = request.POST.get('cuenta')
        contrasena = request.POST.get('contrasena')
        plan = request.POST.get('planes')
        fechaUltimoPago= request.POST.get('fecha')

        # Aquí, podrías realizar cualquier procesamiento adicional si es necesario.

        # Crea una instancia del modelo y guarda los datos en la base de datos.
        nuevo_registro = panelAdmin(
            cuenta=cuenta,
            contrasena=contrasena,
            plan=plan,
            fechaUltimoPago=fechaUltimoPago,
            # Completa con los demás campos
        )
        nuevo_registro.save()

        return redirect('panelAdmin')  # Redirige a la vista que deseas después de guardar el registro

    return render(request, 'panelAdmin/panelAdmin.html')  # Asegúrate de reemplazar 'tu_template.html' con la ruta correcta

def editar_registro(request, id_registro):
    # Recupera el registro específico de la base de datos
    dato = get_object_or_404(panelAdmin, id=id_registro)

     # Lógica para manejar la edición del registro

    # Puedes añadir más lógica aquí si es necesario

    return render(request, 'panelAdmin/panelAdmin.html', {'dato': dato})

def obtener_detalle_registro(request):
    dato_id = request.GET.get('id')
    
    try:
        dato = panelAdmin.objects.get(id=dato_id)
    except panelAdmin.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)

    datos_registro = {
        'cuenta': dato.cuenta,
        'contrasena': dato.contrasena,
        'plan': dato.plan,
        'fechaUltimoPago': str(dato.fechaUltimoPago),
    }
    return JsonResponse(datos_registro)

def actualizar_registro(request):
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        cuenta = request.POST.get('cuenta')
        contrasena = request.POST.get('contrasena')
        plan = request.POST.get('planes')
        fecha_ultimo_pago = request.POST.get('fecha')

        # Obtener el objeto registro desde la base de datos
        registro = get_object_or_404(panelAdmin, id=registro_id)

        # Actualizar los campos del objeto con los nuevos valores
        registro.cuenta = cuenta
        registro.contrasena = contrasena
        registro.plan = plan
        registro.fechaUltimoPago = fecha_ultimo_pago

        # Guardar los cambios en la base de datos
        registro.save()

        # Agregar un mensaje
        messages.success(request, 'Registro actualizado correctamente')

        # Redirigir al usuario a donde desees
        return redirect('panelAdmin')  # Asegúrate de reemplazar 'panelAdmin' con la ruta correcta

    # Si el método no es POST, devolver un error
    messages.error(request, 'Método no permitido')
    return redirect('panelAdmin')  # Otra vez, reemplaza 'panelAdmin' con la ruta correcta

def eliminar_registro(request, id_registro):
    # Obtén el objeto registro desde la base de datos
    registro = get_object_or_404(panelAdmin, id=id_registro)

    if request.method == 'POST':
        # Verifica si el usuario ha confirmado la eliminación
        confirmacion = request.POST.get('confirmacion')

        if confirmacion == 'confirmado':
            # Elimina el registro
            registro.delete()

            # Agrega un mensaje de éxito
            messages.success(request, 'Registro eliminado correctamente')
            
            # Redirige a la página donde se encuentra la tabla de información de cuentas
            return redirect('panelAdmin')  # Reemplaza 'nombre_de_la_vista' con el nombre de la vista que muestra la tabla

    # Renderiza la misma vista con la confirmación
    return render(request, 'panelAdmin/panelAdmin.html', {'registro': registro})
