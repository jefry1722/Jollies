from datetime import date, datetime

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
    if request.method == 'POST':
        agrupacion = Agrupacion.objects.get(id=id)

        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        telefono = request.POST.get("telefono")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        tiempo = request.POST.get("tiempo")
        direccion = request.POST.get("direccion")
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
                                        usuario=usuario, estado="pendiente abono", precio=500000)
            contratacion.save()
        return redirect('abono', id=contratacion.id)
    try:
        usuario = Usuario.objects.get(correo=correo)
        return render(request, 'contratacion.html', {'usuario': usuario})
    except:
        return render(request, 'contratacion.html', {'correo': correo})


def realizarAbono(request, id):
    contratacion = Contratacion.objects.get(id=id)
    abono = contratacion.precio * contratacion.tiempo * 0.1
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
