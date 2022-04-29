"""jollies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from agrupaciones.views import nuevoManager, nuevaAgrupacion, loginManager, menuManager, renovateAccountDate, \
    editarAgrupacion, logout, subirMedia, menuManagerMedia, menuManagerAgrupaciones, menuManagerEditar, menuAgrupacion, \
    verSolicitudesAgrupacion, aprobarContratacion, rechazarContratacion, verRetroalimentaciones, asociarIntegrante, \
    validarCorreoIntegrante, verContratacionesIntegrante
from contrataciones.views import validarCorreo, crearContratacion, realizarAbono, editarContratacion, \
    cancelarContratacion
from usuarios.views import verAgrupaciones, verGeneros, caracteristicasPorAgrupacion, validarCorreoParaContrataciones, \
    historialDeContrataciones, retroalimentarAgrupacion
from web.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='index'),
    path('nuevo_manager', nuevoManager),
    path('nueva_agrupacion', nuevaAgrupacion),
    path('login_manager', loginManager, name='login_manager'),
    path('menu_manager', menuManager, name='menu_manager'),
    path('menu_manager/media', menuManagerMedia),
    path('menu_manager/agrupaciones', menuManagerAgrupaciones),
    path('menu_manager/editar', menuManagerEditar),
    path('renovate', renovateAccountDate, name='renovate'),
    path('editar_agrupacion/<int:id>', editarAgrupacion),
    path('logout', logout),
    path('menu_manager/media/subir/<int:id>', subirMedia),
    path('agrupaciones/<int:id>', verAgrupaciones),
    path('generos', verGeneros, name='generos'),
    path('agrupacion/<int:id>', caracteristicasPorAgrupacion),
    path('validar_correo/<int:id>', validarCorreo),
    path('contratacion/<int:id>/<str:correo>', crearContratacion, name='contratacion'),
    path('contratacion/abono/<int:id>', realizarAbono, name='abono'),
    path('validar_correo_historial', validarCorreoParaContrataciones),
    path('historial/<str:correo>', historialDeContrataciones, name='historial_usuario'),
    path('cancelar_contratacion/<int:id_usuario>/<int:id_contratacion>', cancelarContratacion),
    path('editar_contratacion/<int:id_usuario>/<int:id_contratacion>', editarContratacion),
    path('retroalimentar_agrupacion/<int:id_usuario>/<int:id_contratacion>', retroalimentarAgrupacion),
    path('menu_agrupacion', menuAgrupacion, name='menu_agrupacion'),
    path('menu_agrupacion/solicitudes', verSolicitudesAgrupacion, name='solicitudes_agrupacion'),
    path('menu_agrupacion/aprobar/<int:id>', aprobarContratacion),
    path('menu_agrupacion/rechazar/<int:id>', rechazarContratacion),
    path('menu_agrupacion/retroalimentaciones', verRetroalimentaciones),
    path('menu_agrupacion/asociar_integrante', asociarIntegrante),
    path('validar_correo_integrante', validarCorreoIntegrante),
    path('contrataciones_integrante/<str:correo>', verContratacionesIntegrante, name='contrataciones_integrante'),
]
