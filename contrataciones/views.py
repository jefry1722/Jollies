from django.shortcuts import render

from usuarios.models import Usuario


def contratacion(request, id):
    if request.method == 'POST':
        correo=request.POST.get("correo")
        nombre=request.POST.get("nombre")
        apellido=request.POST.get("apellido")
        telefono=request.POST.get("telefono")
        try:
            usuario=Usuario.get_object_or_404(Usuario, correo=correo)
        except:
            usuario=Usuario(nombre=nombre,correo=correo,apellido=apellido,telefono=telefono)
            usuario.save()
        return render(request,'contratacion.html')
    return render(request, 'contratacion.html')
