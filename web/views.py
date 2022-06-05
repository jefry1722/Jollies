from django.db.models import Avg
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from agrupaciones.models import Agrupacion
from agrupaciones.utils import enviarCorreo
from contrataciones.models import Contratacion
from usuarios.models import Usuario


def inicio(request):
    if request.method == "POST":
        nombre = request.POST.get("name")
        email = request.POST.get("email")
        asunto = request.POST.get("subject")
        mensaje = request.POST.get("message")
        enviarCorreo("jolliesapp@gmail.com", asunto,
                     "Usuario: " + nombre + "\nCorreo: " + email + "\nMensaje: " + mensaje)
    agrupaciones = Agrupacion.objects.order_by('id')
    top_agrupaciones = Contratacion.objects.values('agrupacion__nombre').order_by('agrupacion_id').annotate(
        rating=Avg('rating'))[:3]
    usuarios = Usuario.objects.order_by('id')
    return render(request, 'index.html', {'numero_agrupaciones': len(agrupaciones), 'numero_usuarios': len(usuarios),
                                          'top_agrupaciones': top_agrupaciones})

def terminos(request):
    return render(request,'terminos.html')
