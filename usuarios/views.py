from django.shortcuts import render, redirect, get_object_or_404
from agrupaciones.models import Agrupacion, Genero, Media


def verAgrupaciones(request, id):
    agrupaciones = Agrupacion.objects.filter(genero_id=id)
    if len(agrupaciones) == 0:
        return render(request, 'menu_usuario_agrupaciones.html', {'swal_error_agrupaciones': True})
    if request.method == 'POST':
        agrupacion = request.POST.get("agrupacion")
        agrupacioneFiltradas = Agrupacion.objects.filter(nombre__icontains=agrupacion, genero_id=id)
        if len(agrupacioneFiltradas) > 0:
            return render(request, 'menu_usuario_agrupaciones.html', {'agrupaciones': agrupacioneFiltradas})
        return render(request, 'menu_usuario_agrupaciones.html', {'agrupaciones': agrupaciones, 'swal_error_agrupacion': True})
    return render(request, 'menu_usuario_agrupaciones.html', {'agrupaciones': agrupaciones})


def verGeneros(request):
    generos = Genero.objects.order_by('nombre')
    if request.method == 'POST':
        genero = request.POST.get("genero")
        generosFiltrados = Genero.objects.filter(nombre__icontains=genero)
        if len(generosFiltrados) > 0:
            return render(request, 'menu_usuario_generos.html', {'generos': generosFiltrados})
        return render(request, 'menu_usuario_generos.html', {'generos': generos, 'swal_error_generos': True})
    return render(request, 'menu_usuario_generos.html', {'generos': generos})


def caracteristicasPorAgrupacion(request, id):
    try:
        agrupacion = get_object_or_404(Agrupacion, pk=id)
        precio = "{:,}".format(agrupacion.precio).replace(",", ".")
        agrupacionMedia = Media.objects.filter(agrupacion_id=id)
        return render(request, 'menu_usuario_caracteristicas.html',
                      {'agrupacion': agrupacion, 'precio': precio, 'agrupacionMedia': agrupacionMedia})
    except:
        return redirect('generos')

def verMenuUsuarios(request):
    return render(request, 'menu_usuario_agrupaciones.html')
