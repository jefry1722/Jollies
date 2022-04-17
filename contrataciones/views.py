from datetime import date, datetime, timedelta

from django.db.models import Q
from django.shortcuts import render, redirect

from agrupaciones.models import Agrupacion
from contrataciones.models import Contratacion, Facturacion
from usuarios.models import Usuario


def validarCorreo(request, id):
    if request.method == 'POST':
        correo = request.POST.get("correo")
        return redirect('contratacion', id=id, correo=correo)
    return render(request, 'validacion_correo.html')


def crearContratacion(request, id, correo):
    fecha_actual = date.today()
    hora_actual_mas_3_horas = (datetime.now() + timedelta(hours=3)).strftime("%H:%M")
    swal_error_fecha = False
    swal_error_fecha_contratacion = False
    if request.method == 'POST':
        agrupacion = Agrupacion.objects.get(id=id)

        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        telefono = request.POST.get("telefono")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        tiempo = request.POST.get("tiempo")
        direccion = request.POST.get("direccion")

        # Validar si la agrupación tiene otra contratación con 1 hora y 30 minutos de anticipación
        hora_actual_mas_1_30_horas = (datetime.now() + timedelta(hours=1.5)).strftime("%H:%M")
        contrataciones = Contratacion.objects.filter(~Q(estado__in=["cancelado"]), agrupacion=agrupacion,
                                                     fecha__gte=fecha_actual)
        for contratacion in contrataciones:
            if contratacion.fecha.__str__() == fecha and datetime.strptime(hora, "%H:%M").strftime(
                    "%H:%M") <= hora_actual_mas_1_30_horas:
                swal_error_fecha_contratacion = True
                break

        # Validar si la contratacion es en la misma fecha y con 3 horas de anticipacion
        if fecha == fecha_actual.__str__() and datetime.strptime(hora, "%H:%M").strftime(
                "%H:%M") <= hora_actual_mas_3_horas:
            swal_error_fecha = True
        elif swal_error_fecha_contratacion:
            True
        else:
            try:
                usuario = Usuario.objects.get(correo=correo)
                contratacion = Contratacion(fecha=fecha, hora=hora, tiempo=tiempo, direccion=direccion,
                                            agrupacion=agrupacion,
                                            usuario=usuario, estado="pendiente abono",
                                            precio=agrupacion.precio * int(tiempo))
                contratacion.save()
            except:
                usuario = Usuario(correo=correo, nombre=nombre, apellido=apellido, telefono=telefono)
                usuario.save()
                contratacion = Contratacion(fecha=fecha, hora=hora, tiempo=tiempo, direccion=direccion,
                                            agrupacion=agrupacion,
                                            usuario=usuario, estado="pendiente abono",
                                            precio=agrupacion.precio * int(tiempo))
                contratacion.save()
            return redirect('abono', id=contratacion.id)

    try:
        usuario = Usuario.objects.get(correo=correo)
        return render(request, 'contratacion.html', {'usuario': usuario, 'fecha_actual': fecha_actual.__str__(),
                                                     'swal_error_fecha': swal_error_fecha,
                                                     'swal_error_fecha_contratacion': swal_error_fecha_contratacion})
    except:
        return render(request, 'contratacion.html',
                      {'correo': correo, 'fecha_actual': fecha_actual.__str__(), 'swal_error_fecha': swal_error_fecha,
                       'swal_error_fecha_contratacion': swal_error_fecha_contratacion})


def cancelarContratacion(request, id_usuario, id_contratacion):
    try:
        contratacion = Contratacion.objects.get(id=id_contratacion, usuario_id=id_usuario)
        contratacion.estado = "cancelado"
        contratacion.save()
        return redirect('index')
    except:
        return redirect('index')


def editarContratacion(request, id_usuario, id_contratacion):
    fecha_actual = date.today()
    hora_actual_mas_3_horas = (datetime.now() + timedelta(hours=3)).strftime("%H:%M")
    swal_error_fecha = False
    swal_error_fecha_contratacion = False
    try:
        usuario = Usuario.objects.get(id=id_usuario)
        contratacion_actual = Contratacion.objects.get(id=id_contratacion)
        if request.method == 'POST':
            agrupacion = Agrupacion.objects.get(id=contratacion_actual.agrupacion.id)

            fecha = request.POST.get("fecha")
            hora = request.POST.get("hora")
            tiempo = request.POST.get("tiempo")
            direccion = request.POST.get("direccion")

            # Validar si la agrupación tiene otra contratación con 1 hora y 30 minutos de anticipación
            hora_actual_mas_1_30_horas = (datetime.now() + timedelta(hours=1.5)).strftime("%H:%M")
            contrataciones = Contratacion.objects.filter(~Q(estado__in=["cancelado"]), agrupacion=agrupacion,
                                                         fecha__gte=fecha_actual)
            for contratacion in contrataciones:
                if contratacion.fecha.__str__() == fecha and datetime.strptime(hora, "%H:%M").strftime(
                        "%H:%M") <= hora_actual_mas_1_30_horas:
                    swal_error_fecha_contratacion = True
                    break

            # Validar si la contratacion es en la misma fecha y con 3 horas de anticipacion
            if fecha == fecha_actual.__str__() and datetime.strptime(hora, "%H:%M").strftime(
                    "%H:%M") <= hora_actual_mas_3_horas:
                swal_error_fecha = True
            elif swal_error_fecha_contratacion:
                True
            else:
                contratacion_actual.fecha = fecha
                contratacion_actual.hora = hora
                contratacion_actual.tiempo = tiempo
                contratacion_actual.direccion = direccion
                contratacion_actual.precio = agrupacion.precio * int(tiempo)
                contratacion_actual.estado = "pendiente abono"
                contratacion_actual.save()
                return redirect('abono', id=contratacion.id)
        return render(request, 'contratacion.html',
                      {'usuario': usuario, 'contratacion': contratacion_actual, 'fecha_actual': fecha_actual.__str__(),
                       'swal_error_fecha': swal_error_fecha,
                       'swal_error_fecha_contratacion': swal_error_fecha_contratacion})
    except:
        return redirect('index')


def realizarAbono(request, id):
    contratacion = Contratacion.objects.get(id=id)
    abono = contratacion.precio * 0.1
    precio = "{:,}".format(abono).replace(",", ".")
    if request.method == 'POST':
        transactionDate = date.today()
        transactionTime = datetime.now().strftime("%H:%M:%S")
        facturaction = Facturacion(abono=abono, fecha=transactionDate, hora=transactionTime, contratacion=contratacion)
        facturaction.save()
        contratacion.estado = "pendiente aprobacion"
        contratacion.save()
        return render(request, 'abono.html', {'abono': precio, 'swal_success_abono': True})
    return render(request, 'abono.html', {'abono': precio})
