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
            return redirect('menu_manager')
    else:
        generos = Genero.objects.order_by('id')
    return render(request, 'nueva_agrupacion.html',{'generos':generos})

def editarAgrupacion(request,id):
    print(id)
    return render(request,'editar_agrupacion.html')

def loginManager(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        try:
            manager = Manager.objects.get(correo=correo)
            if(manager.fecha_renovacion<date.today()):
                return render(request,'login_manager.html',{'expiredDate':True})
            if (check_password_hash(manager.password, passwd)):
                return redirect('menu_manager')
            else:
                print("Contraseña incorrecta")
        except:
            print("No se encontró el correo")
    return render(request, 'login_manager.html')

def menuManager(request):
    manager=Manager.objects.get(id=1)
    agrupaciones=Agrupacion.objects.filter(manager=manager)
    return render(request,'menu_manager.html',{'agrupaciones':agrupaciones})

def renovateAccountDate(request):
    if request.method == "POST":
        start_date = date.today()
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        renovation_date = start_date + timedelta(days=days_in_month)
        manager = Manager.objects.get(id=1)
        manager.fecha_renovacion=renovation_date
        manager.save()
        return render(request,'login_manager.html')

    return render(request,'renovate.html')
