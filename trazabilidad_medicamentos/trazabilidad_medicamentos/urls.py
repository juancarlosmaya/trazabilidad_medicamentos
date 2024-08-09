"""
URL configuration for trazabilidad_medicamentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from .views import inicio, inventario,login

# para importar urls de otras aplicaciones
from django.conf.urls import url,include

# archivos estaticos como .css...
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', inicio),
   ## path('inventario/', inventario),
   ## path(r'login/', login),
    path(r'inventario/', include('inventario.urls')),
   ## path('admin/', include('django_sb_admin.urls')),
   path('admin/', admin.site.urls),
    # autenticación autentificación
    #url(r'^accounts/', include('registration.backends.default.urls'),name='inicio_sesion')
    url(r'^accounts/', include('django_registration.backends.one_step.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls'),name='inicio_sesion'),
]

urlpatterns += staticfiles_urlpatterns()