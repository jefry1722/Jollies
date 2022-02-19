from werkzeug.security import generate_password_hash, check_password_hash
from django.shortcuts import render, redirect

from usuarios.models import Usuario


def nuevoUsuario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        passwd_crypted = generate_password_hash(passwd, 'pbkdf2:sha256', 8)
        telefono = request.POST.get("telefono")
        terminos = request.POST.get("check")

        try:
            usuario = Usuario.objects.get(correo=correo)
            datosRecientes = {'nombre': nombre, 'apellido': apellido,
                              'telefono': telefono, 'error_terminos': "El correo ya se encuentra registrado"}
            return render(request, 'nuevo.html', datosRecientes)
        except:
            if terminos == None:
                datosRecientes = {'nombre': nombre, 'apellido': apellido, 'correo': correo,
                                  'telefono': telefono, 'error_terminos': "Debe aceptar los terminos para continuar"}
                return render(request, 'nuevo.html', datosRecientes)
            else:
                usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, telefono=telefono,
                                  password=passwd_crypted)
                usuario.save()
                return redirect('index')
    return render(request, 'nuevo.html')


def loginUsuario(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        try:
            usuario = Usuario.objects.get(correo=correo)
            if (check_password_hash(usuario.password, passwd)):
                return redirect('index')
            else:
                print("Contraseña incorrecta")
        except:
            print("No se encontró el correo")
    return render(request, 'login.html')
