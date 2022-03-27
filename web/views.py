from django.shortcuts import render

from agrupaciones.models import Agrupacion
from usuarios.models import Usuario


def inicio(request):
    agrupaciones = Agrupacion.objects.order_by('id')
    usuarios = Usuario.objects.order_by('id')
    return render(request, 'index.html', {'numero_agrupaciones': len(agrupaciones), 'numero_usuarios': len(usuarios)})
