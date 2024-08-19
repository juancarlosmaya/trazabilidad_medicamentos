from django.db import models
from django.contrib.auth.models import User
import datetime



class config(models.Model):
    # ip_orion = ['192.168.43.173']
    ip_orion = ['192.168.5.125']
    port_orion = ['1026']
    # lista_estados =['Carga de trabajo','Sin asignar','Asignar estado','Sin asignación','Repuesto disponible en CSA','Pendiente por repuesto','Pendiente por aprobación de cliente','Proceso de cambio','Proceso de reparación','Proceso de reparación en taller','Producto en proceso de cambio','Producto entregado','Producto reparado','Servicio cancelado','Soporte técnico']
    lista_estados =['Carga de trabajo','Repuesto disponible en CSA','Pendiente por repuesto','Pendiente por aprobación de cliente','Proceso de cambio','Proceso de reparación','Proceso de reparación en taller','Producto en proceso de cambio','Producto entregado','Producto reparado','Servicio cancelado','Soporte técnico']
    
    
