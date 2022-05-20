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

from agrupaciones.views import nuevo_manager, nueva_agrupacion, login_manager, menu_manager, renovate_account_date, \
    editar_agrupacion, logout, subir_media, menu_manager_media, menu_manager_agrupaciones, menu_manager_editar, menu_agrupacion, \
    ver_solicitudes_agrupacion, aprobar_contratacion, rechazar_contratacion, ver_retroalimentaciones, asociar_integrante, \
    validar_correo_integrante, ver_contrataciones_integrante, completar_contratacion
from contrataciones.views import validar_correo, crear_contratacion, realizar_abono, editar_contratacion, \
    cancelar_contratacion
from usuarios.views import ver_agrupaciones, ver_generos, caracteristicas_por_agrupacion, validar_correo_para_contrataciones, \
    historial_de_contrataciones, retroalimentar_agrupacion
from web.views import inicio, terminos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='index'),
    path('terminos', terminos, name='terminos'),
    path('nuevo_manager', nuevo_manager),
    path('nueva_agrupacion', nueva_agrupacion),
    path('login_manager', login_manager, name='login_manager'),
    path('menu_manager', menu_manager, name='menu_manager'),
    path('menu_manager/media', menu_manager_media),
    path('menu_manager/agrupaciones', menu_manager_agrupaciones),
    path('menu_manager/editar', menu_manager_editar),
    path('renovate', renovate_account_date, name='renovate'),
    path('editar_agrupacion/<int:id>', editar_agrupacion),
    path('logout', logout),
    path('menu_manager/media/subir/<int:id>', subir_media),
    path('agrupaciones/<int:id>', ver_agrupaciones),
    path('generos', ver_generos, name='generos'),
    path('agrupacion/<int:id>', caracteristicas_por_agrupacion),
    path('validar_correo/<int:id>', validar_correo),
    path('contratacion/<int:id>/<str:correo>', crear_contratacion, name='contratacion'),
    path('contratacion/abono/<int:id>', realizar_abono, name='abono'),
    path('validar_correo_historial', validar_correo_para_contrataciones),
    path('historial/<str:correo>', historial_de_contrataciones, name='historial_usuario'),
    path('cancelar_contratacion/<int:id_usuario>/<int:id_contratacion>', cancelar_contratacion),
    path('editar_contratacion/<int:id_usuario>/<int:id_contratacion>', editar_contratacion),
    path('retroalimentar_agrupacion/<int:id_usuario>/<int:id_contratacion>', retroalimentar_agrupacion),
    path('menu_agrupacion', menu_agrupacion, name='menu_agrupacion'),
    path('menu_agrupacion/solicitudes', ver_solicitudes_agrupacion, name='solicitudes_agrupacion'),
    path('menu_agrupacion/aprobar/<int:id>', aprobar_contratacion),
    path('menu_agrupacion/completar/<int:id>', completar_contratacion),
    path('menu_agrupacion/rechazar/<int:id>', rechazar_contratacion),
    path('menu_agrupacion/retroalimentaciones', ver_retroalimentaciones),
    path('menu_agrupacion/asociar_integrante', asociar_integrante),
    path('validar_correo_integrante', validar_correo_integrante),
    path('contrataciones_integrante/<str:correo>', ver_contrataciones_integrante, name='contrataciones_integrante'),
]
