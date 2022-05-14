from datetime import date, timedelta
import calendar
import re
import cloudinary.uploader
from django.views.decorators.http import require_http_methods
from werkzeug.security import generate_password_hash, check_password_hash
from django.shortcuts import render, redirect, get_object_or_404

from agrupaciones.models import Manager, Agrupacion, Genero, Media, Integrante
from agrupaciones.utils import enviarCorreo
from contrataciones.models import Contratacion
from twilio.rest import Client

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def embed_url(video_url):
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
    return re.sub(regex, r"https://www.youtube.com/embed/\1", video_url)


def validate_manager_session(request):
    if "manager_id" not in request.session:
        return False
    return True


def validate_agrupacion_session(request):
    if "agrupacion_id" not in request.session:
        return False
    return True


@require_http_methods(["POST", "GET"])
def nuevo_manager(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        confirmed_passwd = request.POST.get("passwd2")

        datosRecientes = {'nombre': nombre, 'apellido': apellido, 'correo': correo,
                          'swal_error_password': True}
        if passwd != confirmed_passwd:
            return render(request, 'nuevo_manager.html', datosRecientes)

        passwd_crypted = generate_password_hash(passwd, 'pbkdf2:sha256', 8)
        start_date = date.today()
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        renovation_date = start_date + timedelta(days=days_in_month)

        try:
            manager = Manager.objects.get(correo=correo)
            datosRecientes = {'nombre': nombre, 'apellido': apellido,
                              "swal_error_mail": True}
            return render(request, 'nuevo_manager.html', datosRecientes)
        except:
            manager = Manager(nombre=nombre, apellido=apellido, correo=correo, password=passwd_crypted,
                              fecha_renovacion=renovation_date)
            manager.save()
            request.session["manager_id"] = str(manager.id)
            return redirect('menu_manager')

    return render(request, 'nuevo_manager.html')


@require_http_methods(["POST", "GET"])
def nueva_agrupacion(request):
    if not validate_manager_session(request):
        return redirect('index')
    generos = Genero.objects.order_by('id')
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        integrantes = request.POST.get("integrantes")
        genero_id = request.POST.get("genero")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        genero = get_object_or_404(Genero, pk=genero_id)
        passwd = request.POST.get("passwd")
        confirmed_passwd = request.POST.get("passwd2")

        datosRecientes = {'nombre': nombre, 'telefono': telefono, 'correo': correo, 'integrantes': integrantes,
                          'generos': generos, 'precio': precio,
                          'swal_error_password': True}

        if passwd != confirmed_passwd:
            return render(request, 'nueva_agrupacion.html', datosRecientes)
        passwd_crypted = generate_password_hash(passwd, 'pbkdf2:sha256', 8)

        try:
            agrupacion = Agrupacion.objects.get(correo=correo)
            datosRecientes = {'nombre': nombre, 'telefono': telefono, 'integrantes': integrantes, 'generos': generos,
                              'precio': precio,
                              'swal_error_mail': True}
            return render(request, 'nueva_agrupacion.html', datosRecientes)
        except:
            agrupacion = Agrupacion(nombre=nombre, correo=correo, telefono=telefono, descripcion=descripcion,
                                    password=passwd_crypted, genero=genero,
                                    manager_id=int(request.session["manager_id"]), integrantes=integrantes,
                                    precio=precio)
            agrupacion.save()
            return redirect('menu_manager')
    return render(request, 'nueva_agrupacion.html', {'generos': generos})


@require_http_methods(["POST", "GET"])
def editar_agrupacion(request, id):
    if not validate_manager_session(request):
        return redirect('index')
    agrupacion = get_object_or_404(Agrupacion, pk=id)
    manager = Manager.objects.get(id=request.session["manager_id"])
    if agrupacion.manager.id != manager.id:
        return redirect('index')
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        integrantes = request.POST.get("integrantes")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        agrupacion = Agrupacion.objects.get(id=id)
        agrupacion.nombre = nombre
        agrupacion.telefono = telefono
        agrupacion.integrantes = integrantes
        agrupacion.descripcion = descripcion
        agrupacion.precio = precio
        agrupacion.save()
        return redirect('menu_manager')

    descripcion = ""
    if agrupacion.descripcion is not None:
        descripcion = agrupacion.descripcion
    return render(request, 'nueva_agrupacion.html', {'editablePage': True,
                                                     'correo': agrupacion.correo, 'nombre': agrupacion.nombre,
                                                     'integrantes': agrupacion.integrantes,
                                                     'telefono': agrupacion.telefono, 'descripcion': descripcion,
                                                     'precio': agrupacion.precio})


@require_http_methods(["POST", "GET"])
def login_manager(request):
    if "manager_id" in request.session:
        return redirect('menu_manager')
    if "agrupacion_id" in request.session:
        return redirect('menu_agrupacion')

    if request.method == "POST":
        correo = request.POST.get("correo")
        passwd = request.POST.get("passwd")
        usuario = request.POST.get("usuario")

        if usuario == 'manager':
            try:
                manager = Manager.objects.get(correo=correo)
                if (check_password_hash(manager.password, passwd)):
                    request.session["manager_id"] = str(manager.id)
                    if (manager.fecha_renovacion < date.today()):
                        return redirect('renovate')
                    return redirect('menu_manager')
                return render(request, 'login_manager.html', {'swal_error_password': True})
            except:
                return render(request, 'login_manager.html', {'swal_error_mail': True})

        if usuario == 'agrupacion':
            try:
                agrupacion = Agrupacion.objects.get(correo=correo)
                if (check_password_hash(agrupacion.password, passwd)):
                    request.session["agrupacion_id"] = str(agrupacion.id)
                    return redirect('menu_agrupacion')
                return render(request, 'login_manager.html', {'swal_error_password': True})
            except:
                return render(request, 'login_manager.html', {'swal_error_mail': True})
    return render(request, 'login_manager.html')


@require_http_methods(["POST", "GET"])
def menu_manager(request):
    if not validate_manager_session(request):
        return redirect('index')
    manager = Manager.objects.get(id=request.session["manager_id"])
    return render(request, 'menu_manager.html', {'manager': manager})


@require_http_methods(["POST", "GET"])
def menu_manager_media(request):
    if not validate_manager_session(request):
        return redirect('index')
    manager = Manager.objects.get(id=request.session["manager_id"])
    agrupaciones = Agrupacion.objects.filter(manager=manager)
    return render(request, 'menu_manager_media.html', {'agrupaciones': agrupaciones})


@require_http_methods(["POST", "GET"])
def menu_manager_agrupaciones(request):
    if not validate_manager_session(request):
        return redirect('index')
    manager = Manager.objects.get(id=request.session["manager_id"])
    agrupaciones = Agrupacion.objects.filter(manager=manager)
    return render(request, 'menu_manager_agrupaciones.html', {'agrupaciones': agrupaciones})


@require_http_methods(["POST", "GET"])
def menu_manager_editar(request):
    if not validate_manager_session(request):
        return redirect('index')
    manager = Manager.objects.get(id=request.session["manager_id"])
    agrupaciones = Agrupacion.objects.filter(manager=manager)
    return render(request, 'menu_manager_editar.html', {'agrupaciones': agrupaciones})


@require_http_methods(["POST", "GET"])
def renovate_account_date(request):
    if not validate_manager_session(request):
        return redirect('index')
    if request.method == "POST":
        start_date = date.today()
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        renovation_date = start_date + timedelta(days=days_in_month)
        manager = Manager.objects.get(id=request.session["manager_id"])
        manager.fecha_renovacion = renovation_date
        manager.save()
        return redirect('login_manager')

    return render(request, 'renovate.html')


@require_http_methods(["POST", "GET"])
def logout(request):
    if request.session.has_key("manager_id"):
        request.session.flush()
    if request.session.has_key("agrupacion_id"):
        request.session.flush()
    return redirect('index')


@require_http_methods(["POST", "GET"])
def subir_media(request, id):
    if not validate_manager_session(request):
        return redirect('index')
    agrupacion = get_object_or_404(Agrupacion, pk=id)
    manager = Manager.objects.get(id=request.session["manager_id"])
    if agrupacion.manager.id != manager.id:
        return redirect('index')
    if request.method == "POST":
        imagen = request.POST.get("image_base_64")
        video = request.POST.get("video_to_upload")

        media_por_agrupacion = Media.objects.filter(agrupacion=agrupacion)
        if len(media_por_agrupacion) == 3:
            return render(request, 'menu_manager_media_subir.html', {'swal_error': True})

        if imagen is not None:
            cloudinary_response = cloudinary.uploader.upload(imagen)
            media = Media(tipo="imagen", url=cloudinary_response['secure_url'], agrupacion=agrupacion)
            media.save()
            return render(request, 'menu_manager_media_subir.html', {'swal_image_uploaded': True})
        if video is not None and video != '':
            video = embed_url(video)
            media = Media(tipo="video", url=video, agrupacion=agrupacion)
            media.save()
            return render(request, 'menu_manager_media_subir.html', {'swal_video_uploaded': True})
    return render(request, 'menu_manager_media_subir.html')


@require_http_methods(["POST", "GET"])
def menu_agrupacion(request):
    if not validate_agrupacion_session(request):
        return redirect('index')
    agrupacion = Agrupacion.objects.get(id=request.session["agrupacion_id"])
    first = str(agrupacion.telefono)[0:3]
    second = str(agrupacion.telefono)[3:6]
    third = str(agrupacion.telefono)[6:10]
    phone = first + '-' + second + '-' + third
    precio = "{:,}".format(agrupacion.precio).replace(",", ".")
    return render(request, 'menu_agrupacion.html', {'agrupacion': agrupacion, 'telefono': phone, 'precio': precio})


@require_http_methods(["POST", "GET"])
def ver_solicitudes_agrupacion(request):
    if not validate_agrupacion_session(request):
        return redirect('index')
    # Envio de ubicación
    if request.method == 'POST':
        id_contratacion = request.POST.get("id")
        latitud = request.POST.get("lat")
        longitud = request.POST.get("lon")

        contratacion = Contratacion.objects.get(id=id_contratacion)
        account_sid = env('ACCOUNT_SID')
        auth_token = env('AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Ubicación: ' + contratacion.agrupacion.nombre,
            to='whatsapp:+57' + contratacion.usuario.telefono,
            persistent_action="geo:" + latitud + "," + longitud
        )
    fecha_actual = date.today()
    agrupacion = Agrupacion.objects.get(id=request.session["agrupacion_id"])
    contrataciones = Contratacion.objects.filter(agrupacion=agrupacion)
    return render(request, 'menu_agrupacion_solicitudes.html',
                  {'contrataciones': contrataciones, 'fecha_actual': fecha_actual})


@require_http_methods(["POST", "GET"])
def aprobar_contratacion(request, id):
    if not validate_agrupacion_session(request):
        return redirect('index')
    try:
        contratacion = Contratacion.objects.get(id=id, agrupacion_id=request.session["agrupacion_id"])
        contratacion.estado = "pendiente abono"
        contratacion.save()
        mensaje = "La agrupación: " + contratacion.agrupacion.nombre + " ha aprobado tu contratación.\nPara el dia: " + contratacion.fecha.__str__() + " a las " + contratacion.hora.__str__() + ".\nEn tu ubicación: " + contratacion.direccion + "\n¡Ahora puedes realizar tu abono!"
        enviarCorreo(contratacion.usuario.correo, "SE HA APROBADO TU CONTRATACIÓN", mensaje)
        return redirect('solicitudes_agrupacion')
    except:
        return redirect('index')


@require_http_methods(["POST", "GET"])
def completar_contratacion(request, id):
    if not validate_agrupacion_session(request):
        return redirect('index')
    try:
        contratacion = Contratacion.objects.get(id=id, agrupacion_id=request.session["agrupacion_id"])
        contratacion.estado = "completado"
        contratacion.save()
        mensaje = "La agrupación: " + contratacion.agrupacion.nombre + " ha completado el servicio.\nAhora puedes realizar la retroalimentación de tu contratación."
        enviarCorreo(contratacion.usuario.correo, "SE HA COMPLETADO TU CONTRATACIÓN", mensaje)
        return redirect('solicitudes_agrupacion')
    except:
        return redirect('index')


@require_http_methods(["POST", "GET"])
def rechazar_contratacion(request, id):
    if not validate_agrupacion_session(request):
        return redirect('index')
    if request.method == "POST":
        comentario = request.POST.get("comentario")
        try:
            contratacion = Contratacion.objects.get(id=id, agrupacion_id=request.session["agrupacion_id"])
            contratacion.estado = "rechazado"
            contratacion.save()
            mensaje = "La agrupación: " + contratacion.agrupacion.nombre + " ha rechazado tu contratación.\nPara el dia: " + contratacion.fecha.__str__() + " a las " + contratacion.hora.__str__() + ".\nEn tu ubicación: " + contratacion.direccion
            if comentario is not None:
                mensaje += "\nRazón: " + comentario
            enviarCorreo(contratacion.usuario.correo, "SE HA RECHAZADO TU CONTRATACIÓN", mensaje)
            return redirect('solicitudes_agrupacion')
        except:
            return redirect('index')

    return render(request, 'menu_agrupacion_cancelar.html')


@require_http_methods(["POST", "GET"])
def ver_retroalimentaciones(request):
    if not validate_agrupacion_session(request):
        return redirect('index')
    contrataciones = Contratacion.objects.filter(rating__isnull=False, agrupacion_id=request.session["agrupacion_id"])
    return render(request, 'menu_agrupacion_retroalimentaciones.html', {'contrataciones': contrataciones})


@require_http_methods(["POST", "GET"])
def validar_correo_integrante(request):
    if request.method == 'POST':
        correo = request.POST.get("correo")
        return redirect('contrataciones_integrante', correo=correo)
    return render(request, 'validacion_correo_integrante.html')


@require_http_methods(["POST", "GET"])
def asociar_integrante(request):
    if not validate_agrupacion_session(request):
        return redirect('index')
    if request.method == 'POST':
        correo = request.POST.get("correo")
        agrupacion = Agrupacion.objects.get(id=request.session["agrupacion_id"])
        try:
            integrante = Integrante.objects.get(correo=correo)
            return render(request, 'menu_agrupacion_nuevo_integrante.html', {'swal_error_correo': True})
        except:
            integrante = Integrante(correo=correo, agrupacion=agrupacion)
            integrante.save()
        return redirect('menu_agrupacion')
    return render(request, 'menu_agrupacion_nuevo_integrante.html')


@require_http_methods(["POST", "GET"])
def ver_contrataciones_integrante(request, correo):
    try:
        integrante = Integrante.objects.get(correo=correo)
        contrataciones = Contratacion.objects.filter(agrupacion=integrante.agrupacion)
        return render(request, 'contrataciones_integrante.html', {'contrataciones': contrataciones})
    except:
        return redirect('index')
