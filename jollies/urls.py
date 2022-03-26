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
    editarAgrupacion, logout, subirMedia, menuManagerMedia, menuManagerAgrupaciones, menuManagerEditar
from web.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='index'),
    path('nuevo_manager', nuevoManager),
    path('nueva_agrupacion',nuevaAgrupacion),
    path('login_manager',loginManager,name='login_manager'),
    path('menu_manager',menuManager,name='menu_manager'),
    path('menu_manager/media', menuManagerMedia),
    path('menu_manager/agrupaciones', menuManagerAgrupaciones),
    path('menu_manager/editar', menuManagerEditar),
    path('renovate',renovateAccountDate,name='renovate'),
    path('editar_agrupacion/<int:id>',editarAgrupacion),
    path('logout',logout),
    path('subir_media/<int:id>',subirMedia),
]
