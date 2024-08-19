"""
URL configuration for Sertek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from login import views as login
from home import views as home
from logout import views as logout
from cliente_proveedor import views as cliente_proveedor
from crea_contacto import views as crea_contacto
from crear_servicio import views as crear_servicio
from usuarios import views as usuarios
from dashboard import views as dashboard
from facturacion import views as facturacion
from inventario import views as inventario
from pagos import views as pagos
from mensajes import views as mensajes

urlpatterns = [
    path("admin/", admin.site.urls),  # ok
    path('login', login.login, name='login'),  #ok
    path('home', home.home, name='home'), #ok
    path('home/cambio_ciudad', home.cambio_ciudad, name='cambio_ciudad'), #ok
    path('home/ciudad_actual', home.ciudad_actual, name='ciudad_actual'),  #ok
    path('logout', logout.logout, name='logout'), #ok

    path('dashboard', dashboard.dashboard, name='dashboard'), #ok
    path('dashboard/buscar_servicios_filtro', dashboard.buscar_servicios_filtro, name='buscar_servicios_filtro'), #ok Falta filtrar por estado actual para sacar datos del dashboard

    path('cliente_proveedor', cliente_proveedor.cliente_proveedor, name='cliente_proveedor'), #ok
    path('cliente_proveedor/crear_contacto', cliente_proveedor.crear_contacto, name='crear_contacto'), #ok
    path('cliente_proveedor/busca_contactos', cliente_proveedor.busca_contactos, name='busca_contactos'), #ok
    path('cliente_proveedor/eliminar_contacto', cliente_proveedor.eliminar_contacto, name='eliminar_contacto'),  #ok
    path('cliente_proveedor/editar_contacto', cliente_proveedor.editar_contacto, name='editar_contacto'), #ok

    path('usuarios', usuarios.usuarios, name='usuarios'), #ok

    


    # path('crea_contacto', crea_contacto.crea_contacto, name='crea_contacto'),
    path('crear_servicio', crear_servicio.crear_servicio, name='crear_servicio'), #ok
    path('crear_servicio/lista_modelos', crear_servicio.lista_modelos, name='lista_modelos'), #ok
    path('crear_servicio/search_cliente', crear_servicio.search_cliente, name='search_cliente'), #ok
    path('crear_servicio/search_modelo', crear_servicio.search_modelo, name='search_modelo'),#ok
    path('crear_servicio/crear_cliente', crear_servicio.crear_cliente, name='crear_cliente'), #ok
    path('crear_servicio/crear_modelo', crear_servicio.crear_modelo, name='crear_modelo'), #ok
    path('crear_servicio/buscar_clientes', crear_servicio.buscar_clientes, name='buscar_clientes'), #ok
    path('crear_servicio/crear_nuevo_servicio', crear_servicio.crear_nuevo_servicio, name='crear_nuevo_servicio'),#ok
    path('crear_servicio/buscar_servicios_filtro', crear_servicio.buscar_servicios_filtro, name='buscar_servicios_filtro'),#ok
    path('crear_servicio/lista_tecnicos', crear_servicio.lista_tecnicos, name='lista_tecnicos'), # ok
    path('crear_servicio/lista_tecnicos_lugar', crear_servicio.lista_tecnicos_lugar, name='lista_tecnicos_lugar'), #ok
    path('crear_servicio/asigna_tecnico', crear_servicio.asigna_tecnico, name='asigna_tecnico'), #ok
    path('crear_servicio/ver_servicio', crear_servicio.ver_servicio, name='ver_servicio'), #ok
    path('crear_servicio/crea_abono', crear_servicio.crea_abono, name='crea_abono'), #ok
    path('crear_servicio/crea_mensaje', crear_servicio.crea_mensaje, name='crea_mensaje'), #ok
    path('crear_servicio/update_mensaje', crear_servicio.update_mensaje, name='update_mensaje'), #ok
    path('crear_servicio/lista_detalle_abonos', crear_servicio.lista_detalle_abonos, name='lista_detalle_abonos'), #ok
    path('crear_servicio/lista_partes', crear_servicio.lista_partes, name='lista_partes'), #ok
    path('crear_servicio/crea_solicitud_parte', crear_servicio.crea_solicitud_parte, name='crea_solicitud_parte'), #ok
    path('crear_servicio/imprime_orden_servicio', crear_servicio.imprime_orden_servicio, name='imprime_orden_servicio'), #ok
    path('crear_servicio/elimina_solicitud_parte', crear_servicio.elimina_solicitud_parte, name='elimina_solicitud_parte'), #ok
    path('crear_servicio/elimina_abono', crear_servicio.elimina_abono, name='elimina_abono'), #ok 
    path('crear_servicio/actualiza_servicio', crear_servicio.actualiza_servicio, name='actualiza_servicio'), #ok
    path('crear_servicio/crea_remision', crear_servicio.crea_remision, name='crea_remision'), # ok 
    path('crear_servicio/update_remision', crear_servicio.update_remision, name='update_remision'), #ok
    path('crear_servicio/elimina_remision', crear_servicio.elimina_remision, name='elimina_remision'), #ok
    path('crear_servicio/imprime_remision', crear_servicio.imprime_remision, name='imprime_remision'), # ok
    path('crear_servicio/crea_estado', crear_servicio.crea_estado, name='crea_estado'), #ok
    path('crear_servicio/update_estado_panel', crear_servicio.update_estado_panel, name='update_estado_panel'), #ok
    path('crear_servicio/elimina_estado', crear_servicio.elimina_estado, name='elimina_estado'), #ok

    path('facturacion/remision', facturacion.facturacion_remision, name='facturacion_remision'), #ok
    path('facturacion/busca_remision', facturacion.busca_remision, name='busca_remision'), #ok

    path('inventario', inventario.inventario, name='inventario'), #ok
    path('inventario/buscar_items_filtro', inventario.buscar_items_filtro, name='buscar_items_filtro'), #ok
    path('inventario/crear_item', inventario.crear_item, name='crear_item'), #ok
    path('inventario/elimina_item', inventario.elimina_item, name='elimina_item'), #ok
    path('inventario/editar_item', inventario.editar_item, name='editar_item'), #ok


    path('pagos', pagos.pagos, name='pagos'), # Ok
    path('pagos/search', pagos.search, name='pagos_search'), #ok
    path('pagos/get_partes', pagos.get_partes, name='get_partes'), #ok
    path('pagos/carga_valor', pagos.carga_valor, name='carga_valor'), #ok
    path('pagos/realiza_pago', pagos.realiza_pago, name='realiza_pago'), #ok

    path('mensajes', mensajes.mensajes, name='mensajes'), # ok
    path('mensajes/get_global_message', mensajes.get_global_message, name='get_global_message'), # ok
    path('mensajes/set_global_message', mensajes.set_global_message, name='set_global_message'), # ok
]
