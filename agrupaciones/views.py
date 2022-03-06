from datetime import date,timedelta
import calendar
from werkzeug.security import generate_password_hash, check_password_hash
from django.shortcuts import render, redirect, get_object_or_404

from agrupaciones.models import Manager, Agrupacion, Genero


def nuevoManager(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        passwd_crypted = generate_password_hash(passwd, 'pbkdf2:sha256', 8)
        start_date = date.today()
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        renovation_date = start_date + timedelta(days=days_in_month)

        try:
            manager = Manager.objects.get(correo=correo)
            datosRecientes = {'nombre': nombre, 'apellido': apellido,
                              'error_terminos': "El correo ya se encuentra registrado"}
            return render(request, 'nuevo_manager.html', datosRecientes)
        except:
            manager = Manager(nombre=nombre, apellido=apellido, correo=correo, password=passwd_crypted, fecha_renovacion=renovation_date)
            manager.save()
            return redirect('index')

    return render(request, 'nuevo_manager.html')

def nuevaAgrupacion(request):
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        integrantes = request.POST.get("integrantes")
        genero_id=request.POST.get("genero")
        genero = get_object_or_404(Genero, pk=genero_id)
        passwd = request.POST.get("passwd")
        passwd_crypted = generate_password_hash(passwd, 'pbkdf2:sha256', 8)

        try:
            agrupacion = Agrupacion.objects.get(correo=correo)
            datosRecientes = {'nombre': nombre, 'telefono':telefono, 'integrantes':integrantes,
                          'error_terminos': "El correo ya se encuentra registrado"}
            return render(request, 'nueva_agrupacion.html', datosRecientes)
        except:
            agrupacion= Agrupacion(nombre=nombre, correo=correo, telefono=telefono,
                                   password= passwd_crypted,genero=genero, manager_id=1, integrantes=integrantes)
            agrupacion.save()
            return redirect('index')
    else:
        generos = Genero.objects.order_by('id')
    return render(request, 'nueva_agrupacion.html',{'generos':generos})
