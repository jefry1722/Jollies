from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from agrupaciones.models import Agrupacion, Genero, Media
from contrataciones.models import Contratacion
from datetime import date, datetime, timedelta
from django.db.models import Q

from usuarios.models import Usuario


def ver_agrupaciones(request, id):
    agrupaciones = Agrupacion.objects.filter(genero_id=id)
    if len(agrupaciones) == 0:
        return render(request, 'menu_usuario_agrupaciones.html', {'swal_error_agrupaciones': True})
    if request.method == 'POST':
        agrupacion = request.POST.get("agrupacion")
        agrupacioneFiltradas = Agrupacion.objects.filter(nombre__icontains=agrupacion, genero_id=id)
        if len(agrupacioneFiltradas) > 0:
            return render(request, 'menu_usuario_agrupaciones.html', {'agrupaciones': agrupacioneFiltradas})
        return render(request, 'menu_usuario_agrupaciones.html',
                      {'agrupaciones': agrupaciones, 'swal_error_agrupacion': True})
    return render(request, 'menu_usuario_agrupaciones.html', {'agrupaciones': agrupaciones})


def ver_generos(request):
    generos = Genero.objects.order_by('nombre')
    if request.method == 'POST':
        genero = request.POST.get("genero")
        generosFiltrados = Genero.objects.filter(nombre__icontains=genero)
        if len(generosFiltrados) > 0:
            return render(request, 'menu_usuario_generos.html', {'generos': generosFiltrados})
        return render(request, 'menu_usuario_generos.html', {'generos': generos, 'swal_error_generos': True})
    return render(request, 'menu_usuario_generos.html', {'generos': generos})


def caracteristicas_por_agrupacion(request, id):
    try:
        agrupacion = get_object_or_404(Agrupacion, pk=id)
        precio = "{:,}".format(agrupacion.precio).replace(",", ".")
        agrupacionMedia = Media.objects.filter(agrupacion_id=id)
        contrataciones = Contratacion.objects.filter(~Q(estado__in=["cancelado", "completado"]), agrupacion_id=id,
                                                     fecha__gte=date.today())
        first = str(agrupacion.telefono)[0:3]
        second = str(agrupacion.telefono)[3:6]
        third = str(agrupacion.telefono)[6:10]
        phone = first + '-' + second + '-' + third
        return render(request, 'menu_usuario_caracteristicas.html',
                      {'agrupacion': agrupacion, 'precio': precio, 'agrupacionMedia': agrupacionMedia,
                       'contrataciones': contrataciones, 'telefono': phone})
    except:
        return redirect('generos')


def validar_correo_para_contrataciones(request):
    if request.method == 'POST':
        correo = request.POST.get("correo")
        return redirect('historial_usuario', correo=correo)
    return render(request, 'validacion_correo.html')


def historial_de_contrataciones(request, correo):
    try:
        usuario = Usuario.objects.get(correo=correo)
        contrataciones = Contratacion.objects.filter(usuario=usuario)
        return render(request, 'menu_usuario_contrataciones.html',
                      {'usuario': usuario, 'contrataciones': contrataciones, 'fecha_actual': date.today(),
                       'hora_actual': (datetime.now() + timedelta(hours=2)).strftime("%H:%M")})
    except:
        return render(request, 'menu_usuario_contrataciones.html', {'swal_error_usuario': True})


def retroalimentar_agrupacion(request, id_usuario, id_contratacion):
    try:
        contratacion = Contratacion.objects.get(id=id_contratacion, usuario_id=id_usuario, estado="completado")
        if request.method == 'POST':
            rating = request.POST.get('rate')
            comentario = request.POST.get('comentario')
            if rating is not None or rating != "":
                contratacion.rating = int(rating)
            if comentario is not None or comentario != "":
                contratacion.calificacion = comentario
            contratacion.save()
            return redirect('index')
        return render(request, 'menu_usuario_retroalimentacion.html')
    except:
        return redirect('index')
