# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Template
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
import requests
import json
import math
import time
import datetime 
import urllib.parse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import random
import ast
from usuarios import models

# Para la generación del PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

from django.conf import settings

from django.http import FileResponse
from django.http import HttpResponse, HttpResponseNotFound


from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]


# Update estado
def update_estado_elimina(entity,atributo,value):
        try:
                # Vamos por value actual de estados
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_solicitud_parte=orden_servicio_dict['estados_historial']['value']
                lista_solicitud_parte_aux=lista_solicitud_parte.split(',')
                # print(lista_solicitud_parte)
                # print(type(value))
                altera_campo=0
                for i in range(1,len(lista_solicitud_parte_aux)): 
                               if (lista_solicitud_parte_aux[i]==value): # Si es igual la sacamos de la lista
                                        lista_solicitud_parte_aux.pop(i)
                                        altera_campo=1
                                        break
                if (altera_campo==1):
                        # Pasamos de lista  a string
                        lista_solicitud_parte_aux_aux=''
                        for i in range(1,len(lista_solicitud_parte_aux)): 
                                lista_solicitud_parte_aux_aux=lista_solicitud_parte_aux_aux+','+lista_solicitud_parte_aux[i]  
                        # print(lista_solicitud_parte_aux_aux) 
                        
                        # lista_mensaje=lista_mensaje+','+str(value)                       
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=lista_solicitud_parte_aux_aux)
                        # print(response.status_code)
                        print('Lista ',lista_solicitud_parte_aux_aux)
                        if (response.status_code) == 204:
                                if lista_solicitud_parte_aux_aux=='':  #*#*#  Si está vacía, la toma como no asignada, ya que no tiene estados asociadoss
                                        # print('asigna a 0')
                                        update_asignar(str(entity),0) 
                                       

                        # Solicita nombre del estado para desactivarlo

                                # Actualizamos el campo activo del estado
                                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+value+'/attrs/'+'activa'+'/value'
                                headers={"Content-Type":"text/plain"}        
                                response=requests.put(url,headers=headers,json=0)
                                if (response.status_code) == 204:
                                        return "El estado fue desvinculado con la orden de servicio"
                                else :
                                        return "El estado fue desvinculado pero no fue inhabilitado"

                        else :
                                return "El estado NO fue desvinculado con la orden de servicio"
                else:
                       return "El estado NO fue desvinculado con la orden de servicio"
        except:
                return "El estado NO fue desvinculado con la orden de servicio"


# Crea entidad de estado  fecha, técnico, estado y orden
def crea_entidad_estado(servicio, fecha_estado,tecnico, estado,usuario,sede):
        try:
                ContextDataJSON={"id": "",
                                "type": "estado",

                                "servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "estado": {
                                "value": "",
                                "type": "String"
                                },
                                "fecha_estado": {
                                "value": "",
                                "type": "DateTime"
                                },
                                "tecnico":{
                                "value": "",
                                "type": "String"
                                },
                                "usuario":{
                                "value": 'Sertek_1',
                                "type": "String"
                                },
                                "activa":{
                                "value": 1,
                                "type": "integer"
                                },
                                "pagado":{
                                "value": 0,
                                "type": "integer"
                                },
                                "valor_pagado":{
                                "value": 0,
                                "type": "integer"
                                },
                                "fecha_pago":{
                                "value": "",
                                "type": "DateTime"
                                },
                                "sede":{
                                "value": '',
                                "type": "String"
                                },
                                "tipo":{
                                "value": "estado",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='estado' 

                ContextDataJSON['servicio']['value']=servicio  
                ContextDataJSON['estado']['value']=estado       
                ContextDataJSON['fecha_estado']['value']=fecha_estado
                ContextDataJSON['fecha_pago']['value']='0001-01-01T00:00:00'  
                ContextDataJSON['tecnico']['value']=tecnico
                ContextDataJSON['usuario']['value']=usuario
                ContextDataJSON['sede']['value']=sede
                
                ContextDataJSON['tipo']['value']='estado' # Para filtrar datos desde fiware orion
                crea_estado=0
                while(crea_estado==0):
                        ContextDataJSON['id']='estado_'+str(servicio)+'_'+str(random.randint(0,1000000))  # Nombre de la entidad abono abono_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad abono abono_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_estado=1
                                # Actualiza último estado
                                update_ultimo_estado(servicio,estado)
                                # url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(servicio)+'/attrs/'+'ultimo_estado'+'/value'
                                # headers={"Content-Type":"text/plain"}  
                                # print(estado)      
                                # response=requests.put(url,headers=headers,json=estado)
                                break
                        else:
                               time.sleep(1)
                # Actualiza orden con el estado
                update_estados_historial(servicio,'estados_historial',ContextDataJSON['id'])
                return "ok" , ContextDataJSON['id']

        except:
                return "El estado NO pudo ser creado",''

# Update estado en orden de servicio
def update_estados_historial(entity,atributo,value):
        try:
                # Vamos por value actual de la solicitud de la orden de servicio para modificarlo y agregarle más solicitudes
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_estado=orden_servicio_dict['estados_historial']['value']
                lista_estado=lista_estado+','+str(value)                       
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=lista_estado)
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "El estado fue vinculado con la orden de servicio"
                else :
                        return "El estado NO fue vinculado con la orden de servicio"
        except:
                return "El estado NO fue vinculado con la orden de servicio"

# Crea remision  y asigna en un servicio
def crea_entidad_remision(servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte,sede):
        try:
                ContextDataJSON={"id": "",
                                "type": "remision",

                                "servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "forma_pago": {
                                "value": "",
                                "type": "String"
                                },
                                "medio_pago":{
                                "value": "",
                                "type": "String"
                                },
                                "fecha_vencimiento":{
                                "value": ' ',
                                "type": "DateTime"
                                },
                                "producto":{
                                "value": '',
                                "type": "String"
                                },
                                "marca":{
                                "value": '',
                                "type": "String"
                                },
                                "identificacion":{
                                "value": '',
                                "type": "String"
                                },
                                "cliente":{
                                "value": '',
                                "type": "String"
                                },
                                "direccion":{
                                "value": '',
                                "type": "String"
                                },
                                "total_abonos":{
                                "value": '',
                                "type": "String"
                                },
                                "subtotal":{
                                "value": '',
                                "type": "String"
                                },
                                "descuento":{
                                "value": '',
                                "type": "String"
                                },
                                "total":{
                                "value": '',
                                "type": "String"
                                },
                                "usuario":{
                                "value": '',
                                "type": "String"
                                },
                                "fecha_creacion":{
                                "value": '',
                                "type": "DateTime"
                                },
                                "remision":{
                                "value": '',
                                "type": "String"
                                },
                                "informacion_parte":{
                                "value": '',
                                "type": "String"
                                },
                                "sede":{
                                "value": '',
                                "type": "String"
                                },
                                "activa":{
                                "value": 1,
                                "type": "integer"
                                },
                                "tipo":{
                                "value": "remision",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='remision' 

                ContextDataJSON['servicio']['value']=servicio        
                ContextDataJSON['forma_pago']['value']=forma_pago
                ContextDataJSON['medio_pago']['value']=medio_pago
                if (fecha_vencimiento==''):
                        ContextDataJSON['fecha_vencimiento']['value']=str(datetime.date.today()) 
                else:
                        ContextDataJSON['fecha_vencimiento']['value']=fecha_vencimiento
                ContextDataJSON['producto']['value']=producto 
                ContextDataJSON['marca']['value']=marca
                ContextDataJSON['identificacion']['value']=identificacion
                ContextDataJSON['cliente']['value']=cliente
                ContextDataJSON['direccion']['value']=direccion
                ContextDataJSON['total_abonos']['value']=total_abonos
                ContextDataJSON['subtotal']['value']=subtotal
                ContextDataJSON['descuento']['value']=descuento
                ContextDataJSON['total']['value']=total
                ContextDataJSON['usuario']['value']=usuario
                ContextDataJSON['sede']['value']=sede
                
                ContextDataJSON['informacion_parte']['value']=informacion_parte
                print("")
                print("")
                print("")
                print("")
                print(informacion_parte)
                print("")
                print("")
                print("")
                # print(len(informacion_parte))

                # print(json.dumps(informacion_parte))

                ContextDataJSON['tipo']['value']='remision' # Para filtrar datos desde fiware orion

                # ContextDataJSON['id']='remision_'+str(servicio) # Nombre de la entidad remision remision_servicio_+randit()
                # ContextDataJSON['remision']['value']=ContextDataJSON['id']

                crea_remision=0
                while(crea_remision==0):
                        ContextDataJSON['id']='remision_'+str(servicio)+'_'+str(random.randint(0,1000000))  # Nombre de la entidad remision remisison_servicio_+randit()
                        ContextDataJSON['remision']['value']=ContextDataJSON['id']
                        ContextDataJSON['fecha_creacion']['value']=str(datetime.date.today()) 

                        # ContextDataJSON['id']='remision_'+str(servicio) # Nombre de la entidad remision remision_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad abono abono_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_remision=1
                                break
                        else:
                               time.sleep(1)

                        # Actualiza la orden de servicio con la remision creada
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(servicio)+'/attrs/'+'remision'+'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=str(ContextDataJSON['id']))
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "La remisión fue vinculada con la orden de servicio " + str(ContextDataJSON['id']) , ContextDataJSON['id']
                else :
                        return "La remisión fue creada pero NO fue vinculada con la orden de servicio", ''


        except:
                return "La remision NO pudo ser creada",''

# Update solicitud de parte en orden de servicio
def update_abono_elimina(entity,atributo,value):
        try:
                # Vamos por value actual de la solicitud de la orden de servicio para modificarlo
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_abonos=orden_servicio_dict['abonos']['value']
                lista_abonos_aux=lista_abonos.split(',')
                print(lista_abonos_aux)
                # print(type(value))
                altera_campo=0
                for i in range(1,len(lista_abonos_aux)): 
                               if (lista_abonos_aux[i]==value): # Si es igual la sacamos de la lista
                                        lista_abonos_aux.pop(i)
                                        altera_campo=1
                                        break
                if (altera_campo==1):
                        # Pasamos de lista  a string
                        lista_abonos_aux_aux=''
                        for i in range(1,len(lista_abonos_aux)): 
                                lista_abonos_aux_aux=lista_abonos_aux_aux+','+lista_abonos_aux[i]  
                        # print(lista_solicitud_parte_aux_aux) 
                        
                        # lista_mensaje=lista_mensaje+','+str(value)                       
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=lista_abonos_aux_aux)
                        # print(response.status_code)
                        if (response.status_code) == 204:
                                return "El abono fue desvinculado de la orden de servicio"
                        else :
                                return "El abono NO fue desvinculado de la orden de servicio"
                else:
                       return "El abono NO fue desvinculado de la orden de servicio debido a que no existe"
        except:
                return "El abono NO fue desvinculado de la orden de servicio"

# Crea solicitud parte y asigna en un servicio
def crea_entidad_solicitud_parte(servicio, nombre_parte,referencia, precio, cantidad,usuario):
        try:
                ContextDataJSON={"id": "",
                                "type": "solicitud_parte",

                                "servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "nombre_parte": {
                                "value": "",
                                "type": "String"
                                },
                                "referencia":{
                                "value": "",
                                "type": "String"
                                },
                                "precio":{
                                "value": 0,
                                "type": "integer"
                                },
                                "cantidad":{
                                "value": 0,
                                "type": "integer"
                                },
                                "fecha_solicitud":{
                                "value": '',
                                "type": "DateTime"
                                },
                                "usuario":{
                                "value": 'Sertek_1',
                                "type": "String"
                                },
                                "tipo":{
                                "value": "solicitud_parte",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='solicitud_parte' 

                ContextDataJSON['servicio']['value']=servicio        
                ContextDataJSON['nombre_parte']['value']=nombre_parte
                ContextDataJSON['referencia']['value']=referencia
                ContextDataJSON['precio']['value']=int(precio)
                ContextDataJSON['cantidad']['value']=int(cantidad) 
                ContextDataJSON['usuario']['value']=usuario
                ContextDataJSON['fecha_solicitud']['value']=str(datetime.date.today()) 
                
                ContextDataJSON['tipo']['value']='solicitud_parte' # Para filtrar datos desde fiware orion
                crea_solicitud=0
                while(crea_solicitud==0):
                        ContextDataJSON['id']='solicitud_parte_'+str(servicio)+'_'+str(random.randint(0,1000000))  # Nombre de la entidad abono abono_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad abono abono_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_solicitud=1
                                break
                        else:
                               time.sleep(1)
                return "ok" , ContextDataJSON['id']

        except:
                return "La solicitud NO pudo ser creada",''
# Update solicitud de parte en orden de servicio
def update_solicitud(entity,atributo,value):
        try:
                # Vamos por value actual de la solicitud de la orden de servicio para modificarlo y agregarle más solicitudes
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_mensaje=orden_servicio_dict['solicitud_parte']['value']
                lista_mensaje=lista_mensaje+','+str(value)                       
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=lista_mensaje)
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "La solicitud de parte fue vinculada con la orden de servicio"
                else :
                        return "La solicitud de parte NO fue vinculada con la orden de servicio"
        except:
                return "La solicitud de parte NO fue vinculada con la orden de servicio"

# Update solicitud de parte en orden de servicio
def update_solicitud_elimina(entity,atributo,value):
        try:
                # Vamos por value actual de la solicitud de la orden de servicio para modificarlo y agregarle más solicitudes
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_solicitud_parte=orden_servicio_dict['solicitud_parte']['value']
                lista_solicitud_parte_aux=lista_solicitud_parte.split(',')
                # print(lista_solicitud_parte)
                # print(type(value))
                altera_campo=0
                for i in range(1,len(lista_solicitud_parte_aux)): 
                               if (lista_solicitud_parte_aux[i]==value): # Si es igual la sacamos de la lista
                                        lista_solicitud_parte_aux.pop(i)
                                        altera_campo=1
                                        break
                if (altera_campo==1):
                        # Pasamos de lista  a string
                        lista_solicitud_parte_aux_aux=''
                        for i in range(1,len(lista_solicitud_parte_aux)): 
                                lista_solicitud_parte_aux_aux=lista_solicitud_parte_aux_aux+','+lista_solicitud_parte_aux[i]  
                        # print(lista_solicitud_parte_aux_aux) 
                        
                        # lista_mensaje=lista_mensaje+','+str(value)                       
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=lista_solicitud_parte_aux_aux)
                        # print(response.status_code)
                        if (response.status_code) == 204:
                                return "La solicitud de parte fue desvinculada con la orden de servicio"
                        else :
                                return "La solicitud de parte NO fue desvinculada con la orden de servicio"
                else:
                       return "La solicitud de parte NO fue desvinculada con la orden de servicio debido a que no existe"
        except:
                return "La solicitud de parte NO fue desvinculada con la orden de servicio"

# Consulta partes
def consulta_partes(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3,atributo_4,valor_4):
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    if valor_4!='Colombia':
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'=='+str(valor_3)+';'+atributo_4+'=='+str(valor_4)+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    else:
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'=='+str(valor_3)+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
            
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        # print(response.status_code)
        if (response.status_code==200):
            try:
                rh = json.dumps(response.headers.__dict__['_store'])
                response_JSON=json.loads(rh)
                total_id=int(response_JSON['fiware-total-count'][1])
                # print(total_id)
                if (total_id!=0):    
                    dict_entidades=response.content.decode("utf-8").replace("'", '"')
                    dict_entidades=json.loads(dict_entidades)
                #     while(total_id>len(dict_entidades)):
                #         # print("hace")
                #         # offset_aux=len(dict_entidades)+offset_aux
                #         url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(len(dict_entidades))
                #         headers={"Accept":"application/json"}
                #         response=requests.get(url,headers=headers)
                #         # print(response)
                #         dict_entidades_aux=response.content.decode("utf-8").replace("'", '"')
                #         dict_entidades_aux=json.loads(dict_entidades_aux)
                #         dict_entidades=dict_entidades+dict_entidades_aux
                # #     print(dict_entidades)
                    return total_id,dict_entidades
                else:
                #     dict_identidades=None
                    dict_identidades=''
                    return total_id,dict_identidades
                   
            except:
                dict_identidades=None
                total_id=0
                return total_id,dict_identidades
            
        else:
            dict_identidades=None
            total_id=0
            return total_id,dict_identidades 
    except:
        dict_identidades=None
        total_id=0
        return total_id,dict_identidades

# Crea mensaje y lo asigna en un servicio
def crea_entidad_mensaje(servicio,mensaje,usuario):
        try:
                ContextDataJSON={"id": "",
                                "type": "mensaje",

                                "servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "mensaje": {
                                "value": "",
                                "type": "String"
                                },
                                "usuario":{
                                "value": "",
                                "type": "String"
                                },
                                "fecha_mensaje":{
                                "value": '',
                                "type": "DateTime"
                                },
                                "tipo":{
                                "value": "mensaje",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='mensaje' 

                ContextDataJSON['servicio']['value']=servicio        
                ContextDataJSON['mensaje']['value']=mensaje
                ContextDataJSON['usuario']['value']=usuario
                now = datetime.datetime.now()
                fecha_hora = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # print(fecha_hora)
                ContextDataJSON['fecha_mensaje']['value']=fecha_hora
                # ContextDataJSON['fecha_mensaje']['value']=str(datetime.datetime.now()) 
                
                ContextDataJSON['tipo']['value']='mensaje' # Para filtrar datos desde fiware orion
                crea_mensaje=0
                while(crea_mensaje==0):
                        ContextDataJSON['id']='mensaje_'+str(servicio)+'_'+str(random.randint(0,1000000))  # Nombre de la entidad mensaje mensaje_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad mensaje mensaje_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_mensaje=1
                                break
                        else:
                               time.sleep(1)
                return "ok" , ContextDataJSON['id']

        except:
                return "El mensaje NO pudo ser creado",''

# Update mensaje en orden de servicio
def update_mensaje_servicio(entity,atributo,value):
        try:
                # Vamos por value actual de abonos de la orden de servicio para modificarlo y agregarle el nuevo abono
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_mensaje=orden_servicio_dict['mensajes']['value']
                lista_mensaje=lista_mensaje+','+str(value)                       
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=lista_mensaje)
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "El mensaje fue vinculado con la orden de servicio"
                else :
                        return "El mensaje NO pudo ser vinculado con la orden de servicio"
        except:
                return "El mensaje NO pudo ser vinculado con la orden de servicio"

# Crea abono y asigna lo pone en un servicio
def crea_entidad_abono(servicio, medio_de_pago,nombre_razon_social, detalle, valor_abono,usuario):
        try:
                ContextDataJSON={"id": "",
                                "type": "abono",

                                "servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "medio_de_pago": {
                                "value": "",
                                "type": "String"
                                },
                                "nombre_razon_social":{
                                "value": "",
                                "type": "String"
                                },
                                "detalle":{
                                "value": "",
                                "type": "String"
                                },
                                "valor_abono":{
                                "value": 0,
                                "type": "integer"
                                },
                                "fecha_abono":{
                                "value": '',
                                "type": "DateTime"
                                },
                                "usuario":{
                                "value": '',
                                "type": "String"
                                },
                                "tipo":{
                                "value": "abono",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='abono' 

                ContextDataJSON['servicio']['value']=servicio        
                ContextDataJSON['medio_de_pago']['value']=medio_de_pago
                ContextDataJSON['nombre_razon_social']['value']=nombre_razon_social
                ContextDataJSON['detalle']['value']=detalle
                ContextDataJSON['usuario']['value']=usuario
                ContextDataJSON['valor_abono']['value']=int(valor_abono) 
                ContextDataJSON['fecha_abono']['value']=str(datetime.date.today()) 
                
                ContextDataJSON['tipo']['value']='abono' # Para filtrar datos desde fiware orion
                crea_abono=0
                while(crea_abono==0):
                        ContextDataJSON['id']='abono_'+str(servicio)+'_'+str(random.randint(0,1000000))  # Nombre de la entidad abono abono_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad abono abono_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_abono=1
                                break
                        else:
                               time.sleep(1)
                return "ok" , ContextDataJSON['id']

        except:
                return "El abono NO pudo ser creado",''

# Update abonos en orden de servicio
def update_abonos_servicio(entity,atributo,value):
        try:
                # Vamos por value actual de abonos de la orden de servicio para modificarlo y agregarle el nuevo abono
                orden_servicio_dict=consulta_entidad(str(entity))
                lista_abonos=orden_servicio_dict['abonos']['value']
                lista_abonos=lista_abonos+','+str(value)
                # print(lista_abonos)                        
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=lista_abonos)
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "El abono fue vinculado con la orden de servicio"
                else :
                        return "El abono NO pudo ser vinculado con la orden de servicio"
        except:
                return "El abono NO pudo ser vinculado con la orden de servicio"
               

# # Agrega técnicos append en la entidad
# def append_attrs(entity,atributo,value,user):
#     try:
#         # Primero vamos por el atributo tecnico 
#         dic_ent=consulta_entidad(str(entity))
#         # tecnico=dic_ent['tecnico']['value'] # Extraemos valor 
#         # print(tecnico)  
#         url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(entity)+'/attrs?options=append'
#         ContextDataJSON={str(atributo): 
#                         {
#                         "value": [str(value),str(user)],
#                         "type": "String"
#                         }
#                         }
#         # headers={"Content-Type":"text/plain"}
#         headers={"Accept":"application/json"}
#         response=requests.post(url,headers=headers,json=ContextDataJSON)
#         # print(response.status_code)
#         # print(type(response.status_code))
        
#         if (response.status_code) == 204:
#                 return "El técnico fue asignado"
#         if (response.status_code) == 422: # El atributo ya existe
#                 return "no"
#         else :
#                 return "El técnico NO fue asignado"
#     except:
#         return "El técnico NO fue asignado, error en la base de datos"

# Actualiza asignar para que ya no salgan cuando se filtran los servicios sin asignar
def update_tecnico(entity,value):
        try:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+'tecnico'+'/value'
                headers={"Content-Type":"text/plain"}        
                response=requests.put(url,headers=headers,json=value)
                if (response.status_code) == 204:
                        return "El técnico fue asignado"
                else :
                        return "El técnico NO pudo ser actualizado"
        except:
                return "El técnico NO pudo ser actualizado"

# Actualiza estado 
def update_ultimo_estado(entity,value):
        try:
                # Actualiza campo estado
                ContextDataJSON={"ultimo_estado": {
                                "value": str(value),
                                "type": "String"
                                }
                                }

                # url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+'estado'+'/value'
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'
                # headers={"Content-Type":"text/plain"} 
                headers={"Accept":"application/json"}       
                # response=requests.put(url,headers=headers,json=str(value))
                response=requests.post(url,headers=headers,json=ContextDataJSON)
                print(response.text)
                if (response.status_code) == 204:
                        return "El estado fue asignado"
                else :
                        return "El estado NO pudo ser actualizado"
        except:
                return "El estado NO pudo ser actualizado"
                        
# Actualiza asignar para que ya no salgan cuando se filtran los servicios sin asignar
def update_asignar(entity,value):
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+'asignar'+'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=value)
                        if (response.status_code) == 204:
                                return "El contacto ha sido actualizado"
                        else :
                                return "El contacto NO pudo ser actualizado"

# Crea un servicio
def crea_servicio(tipo_servicio, lugar, seguimiento, identidad,nombre, direccion, email, localidad, telefono, modelo, marca, producto, serie,doc_ref,falla,accesorios,observacion,asignar,sede):
        try:
                ContextDataJSON={"id": "num_servicio",
                                "type": "contacto",
                                "tipo_servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "num_servicio": {
                                "value": "",
                                "type": "String"
                                },
                                "lugar": {
                                "value": "",
                                "type": "String"
                                },
                                "seguimiento":{
                                "value": "",
                                "type": "String"
                                },
                                "identidad":{
                                "value": "",
                                "type": "String"
                                },
                                "nombre":{
                                "value": "",
                                "type": "String"
                                },
                                "direccion":{
                                "value": "",
                                "type": "String"
                                },
                                "email":{
                                "value": "",
                                "type": "String"
                                },
                                "sede":{
                                "value": "",
                                "type": "String"
                                },
                                "localidad":{
                                "value": "",
                                "type": "String"
                                },
                                "telefono":{
                                "value": "",
                                "type": "String"
                                },
                                "modelo":{
                                "value": "",
                                "type": "String"
                                },
                                "marca":{
                                "value": "",
                                "type": "String"
                                },
                                "producto":{
                                "value": "",
                                "type": "String"
                                },
                                "serie":{
                                "value": "",
                                "type": "String"
                                },
                                "doc_ref":{
                                "value": "",
                                "type": "String"
                                },
                                "falla":{
                                "value": "",
                                "type": "String"
                                },
                                "accesorios":{
                                "value": "",
                                "type": "String"
                                },
                                "observacion":{
                                "value": "",
                                "type": "String"
                                },
                                "fecha":{
                                "value": "",
                                "type": "DateTime"
                                },
                                "tecnico":{
                                "value": "",
                                "type": "String"
                                },
                                "abonos":{
                                "value": '',
                                "type": "String"
                                },
                                "mensajes":{
                                "value": '',
                                "type": "String"
                                },
                                "solicitud_parte":{
                                "value": '',
                                "type": "String"
                                },
                                "asignar":{
                                "value": 0,
                                "type": "integer"
                                },
                                "fecha_estado":{
                                "value": "",
                                "type": "DateTime"
                                },
                                "estado":{
                                "value": "",
                                "type": "String"
                                },
                                "remision":{
                                "value": "",
                                "type": "String"
                                },
                                "estados_historial":{
                                "value": "",
                                "type": "String"
                                },
                                "ultimo_estado":{
                                "value": "",
                                "type": "String"
                                },
                                "tipo":{
                                "value": "servicio",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='servicio'                  
                ContextDataJSON['tipo_servicio']['value']=tipo_servicio        
                ContextDataJSON['lugar']['value']=lugar
                ContextDataJSON['seguimiento']['value']=seguimiento
                ContextDataJSON['identidad']['value']=identidad
                ContextDataJSON['nombre']['value']=nombre 
                ContextDataJSON['direccion']['value']=direccion 

                ContextDataJSON['email']['value']=email 
                ContextDataJSON['localidad']['value']=localidad 
                ContextDataJSON['telefono']['value']=telefono 

                ContextDataJSON['modelo']['value']=modelo
                ContextDataJSON['marca']['value']=marca
                ContextDataJSON['producto']['value']=producto 
                ContextDataJSON['serie']['value']=serie 
                ContextDataJSON['doc_ref']['value']=doc_ref 
                ContextDataJSON['falla']['value']=falla 
                ContextDataJSON['accesorios']['value']=accesorios 
                ContextDataJSON['observacion']['value']=observacion 
                ContextDataJSON['asignar']['value']=asignar 
                ContextDataJSON['sede']['value']=sede 

                ContextDataJSON['estado']['value']='Carga de trabajo'  # Estado por defecto
                ContextDataJSON['ultimo_estado']['value']='Carga de trabajo'  # Estado por defecto
                
                ContextDataJSON['tipo']['value']='servicio' # Para filtrar datos desde fiware orion
                # Hasta que encuentre una entidad vacía
                index_service=0 
                crea_servicio=0
                while(crea_servicio==0):
                        index_service=index_service+1
                        if index_service >=100:
                                message="El servicio NO pudo ser creado"
                                crea_servicio=1
                                break
                        # Vamos por el counter
                        counterservices=consulta_counterservices()
                        # print(counterservices['bogota']['value'])
                        ContextDataJSON['id']=str(int(counterservices[str(sede).replace('á', 'a', 10).replace('é', 'e', 10).replace('í', 'i', 10).replace('ó', 'o', 10).replace('ú', 'u', 10).replace('ñ', 'n', 10)]['value'])+index_service)
                        ContextDataJSON['num_servicio']['value']=ContextDataJSON['id']
                        ContextDataJSON['fecha']['value']=str(datetime.date.today()) 
                        # La fecha de estado es la misma que la de creación al incio
                        ContextDataJSON['fecha_estado']['value']=str(datetime.date.today()) 

                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_servicio=1
                                update_counter('counterservices',str(sede).replace('á', 'a', 10).replace('é', 'e', 10).replace('í', 'i', 10).replace('ó', 'o', 10).replace('ú', 'u', 10).replace('ñ', 'n', 10),int(counterservices[str(sede).replace('á', 'a', 10).replace('é', 'e', 10).replace('í', 'i', 10).replace('ó', 'o', 10).replace('ú', 'u', 10).replace('ñ', 'n', 10)]['value'])+index_service)
                                message="El servicio ha sido creado " + str(int(counterservices[str(sede).replace('á', 'a', 10).replace('é', 'e', 10).replace('í', 'i', 10).replace('ó', 'o', 10).replace('ú', 'u', 10).replace('ñ', 'n', 10)]['value'])+index_service)
                                break
                                # return "El servicio ha sido creado"
                        time.sleep(0.2)
                        # if (response.status_code) == 422:
                        #        message="El servicio ya existe"
                return message
        except:
                return "El servicio no pudo ser creado"

# Consulta counterservices
def consulta_counterservices():
        try:    
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/counterservices'
                headers={"Accept":"application/json"}
                response=requests.get(url,headers=headers)
                status_code=response.status_code
                response=response.content.decode("utf-8").replace("'", '"')
                response_JSON=json.loads(response)
                if (status_code) == 200:
                        return response_JSON
                else :
                        response_JSON=""
                        return response_JSON
        except:
                response_JSON=None              
                return response_JSON
def update_counter(entity,atributo,value):
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'+str(atributo) +'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=str(value))
                        if (response.status_code) == 204:
                                return "El contacto ha sido actualizado"
                        else :
                                return "El contacto NO pudo ser actualizado"
# Crea un contacto
def crea_contacto(tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email):
        try:
                ContextDataJSON={"id": "num_usuario",
                                "type": "contacto",
                                "tipo_contacto": {
                                "value": "Carlos",
                                "type": "String"
                                },
                                "tipo_identidad": {
                                "value": "Bogotá",
                                "type": "String"
                                },
                                "identidad":{
                                "value": "Cll 147 #7g-84",
                                "type": "String"
                                },
                                "nombre":{
                                "value": "1085254913",
                                "type": "String"
                                },
                                "direccion":{
                                "value": "Vigente",
                                "type": "String"
                                },
                                "telefono":{
                                "value": "Vigente",
                                "type": "String"
                                },
                                "departamento":{
                                "value": "Vigente",
                                "type": "String"
                                },
                                "localidad":{
                                "value": "Vigente",
                                "type": "String"
                                },
                                "email":{
                                "value": "usuario",
                                "type": "String"
                                },
                                "tipo":{
                                "value": "usuario",
                                "type": "String"
                                }
                                }
                ContextDataJSON['id']=str(identidad)
                ContextDataJSON['type']='contacto'  
                
                ContextDataJSON['tipo_contacto']['value']=tipo_contacto        
                ContextDataJSON['tipo_identidad']['value']=tipo_identidad
                ContextDataJSON['identidad']['value']=str(identidad) 
                ContextDataJSON['nombre']['value']=nombre 
                ContextDataJSON['direccion']['value']=direccion 
                ContextDataJSON['telefono']['value']=str(telefono) 
                ContextDataJSON['departamento']['value']=departamento 
                ContextDataJSON['localidad']['value']=localidad 
                ContextDataJSON['email']['value']=email 
                
                ContextDataJSON['tipo']['value']='contacto' # Para filtrar datos desde fiware orion
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                headers={"Accept":"application/json"}
                response= requests.post(url,headers=headers,json=ContextDataJSON) 
                # print(response.status_code)
                if (response.status_code) == 201:
                        return "El cliente ha sido creado"
                if (response.status_code) == 422:
                        return "El cliente ya existe"
                # response=response.content.decode("utf-8")
                # print(response)
                # response_JSON=json.loads(response)
                # print(response_JSON)
        except:
                return "El cliente no pudo ser creado"

# # Actualiza atributo de entidad
# def update(entity,tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email):
#         try:    
#                 ContextDataJSON={"tipo_contacto": {
#                                 "value": "Carlos",
#                                 "type": "String"
#                                 },
#                                 "tipo_identidad": {
#                                 "value": "Bogotá",
#                                 "type": "String"
#                                 },
#                                 "identidad":{
#                                 "value": "Cll 147 #7g-84",
#                                 "type": "String"
#                                 },
#                                 "nombre":{
#                                 "value": "1085254913",
#                                 "type": "String"
#                                 },
#                                 "direccion":{
#                                 "value": "Vigente",
#                                 "type": "String"
#                                 },
#                                 "telefono":{
#                                 "value": "Vigente",
#                                 "type": "String"
#                                 },
#                                 "departamento":{
#                                 "value": "Vigente",
#                                 "type": "String"
#                                 },
#                                 "localidad":{
#                                 "value": "Vigente",
#                                 "type": "String"
#                                 },
#                                 "email":{
#                                 "value": "usuario",
#                                 "type": "String"
#                                 },
#                                 "tipo":{
#                                 "value": "usuario",
#                                 "type": "String"
#                                 }
#                                 } 
                
#                 ContextDataJSON['tipo_contacto']['value']=tipo_contacto        
#                 ContextDataJSON['tipo_identidad']['value']=tipo_identidad
#                 ContextDataJSON['identidad']['value']=str(identidad) 
#                 ContextDataJSON['nombre']['value']=nombre 
#                 ContextDataJSON['direccion']['value']=direccion 
#                 ContextDataJSON['telefono']['value']=str(telefono) 
#                 ContextDataJSON['departamento']['value']=departamento 
#                 ContextDataJSON['localidad']['value']=localidad 
#                 ContextDataJSON['email']['value']=email                 
#                 ContextDataJSON['tipo']['value']='contacto' # Para filtrar datos desde fiware orion

#                 url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entity+'/attrs/'
#                 headers={"Accept":"application/json"}      
#                 response=requests.put(url,headers=headers,json=ContextDataJSON)
#                 # print(response.status_code)
#                 if (response.status_code) == 204:
#                         return "El contacto ha sido actualizado"
#                 else :
#                         return "El contacto NO pudo ser actualizado"

#         except:
#                 return "El contacto NO pudo ser actualizado"

# Consulta una entidades por atributo
def consulta_entiti_atributo(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3):
    if valor_2!='Colombia':
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'~='+valor_3+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    else:
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_3+'~='+valor_3+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        if (response.status_code==200):
            try:
                rh = json.dumps(response.headers.__dict__['_store'])
                response_JSON=json.loads(rh)
                total_id=int(response_JSON['fiware-total-count'][1])
                if (total_id!=0):    
                    dict_entidades=response.content.decode("utf-8").replace("'", '"')
                    dict_entidades=json.loads(dict_entidades)
                    return total_id,dict_entidades
                else:
                    dict_identidades=""
                    return total_id,dict_identidades              
            except:
                dict_identidades=None
                total_id=0
                return total_id,dict_identidades         
        else:
            dict_identidades=None
            total_id=0
            return total_id,dict_identidades 
    except:
        dict_identidades=None
        total_id=0
        return total_id,dict_identidades

# # Elimina entidad
# def borra_entidad(id_entyti):
#         try:
#                 url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+id_entyti
#                 headers={"Accept":"application/json"}
#                 response=requests.delete(url,headers=headers)
#                 if (response.status_code) == 204:
#                         return "El contacto ha sido eliminado"
#                 else :
#                         return "El contacto NO pudo ser eliminado"
#         except:
#                return "La contacto NO pudo ser eliminado"

# Consulta una entidad específica
def consulta_entidad(entidad):
        try:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(entidad)
                headers={"Accept":"application/json"}
                response=requests.get(url,headers=headers)
                status_code=response.status_code
                response=response.content.decode("utf-8").replace("'", '"')
                response_JSON=json.loads(response)
                if (status_code) == 200:
                        return response_JSON
                else :
                        response_JSON=""
                        return response_JSON
        except:              
                response_JSON=None
                return response_JSON

# Consulta una entidad específica
def consulta_modelo(modelo):
        try:    
                # Reemplazamos los caracteres prohibidos para las entidades
                modelo=modelo.replace('/', '*', 10)
                modelo=modelo.replace(' ', '_', 10) 
                # print(urllib.parse.quote(str(modelo),safe=''))
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(modelo)
                headers={"Accept":"application/json"}
                response=requests.get(url,headers=headers)
                status_code=response.status_code
                response=response.content.decode("utf-8").replace("'", '"')
                response_JSON=json.loads(response)
                if (status_code) == 200:
                        # Reemplazamos los caracteres prohibidos para las entidades
                        response_JSON['id']=response_JSON['id'].replace('*', '/', 10)
                        response_JSON['id']=response_JSON['id'].replace('_', ' ', 10) 
                        return response_JSON
                else :
                        response_JSON=""
                        return response_JSON
        except:
                response_JSON=None              
                return response_JSON

# # Crea un modelo
def crea_modelo(marca,producto,nombre_producto):
        try:    
                # Reemplazamos los caracteres prohibidos para las entidades
                nombre_producto=nombre_producto.replace('/', '*', 10)
                nombre_producto=nombre_producto.replace(' ', '_', 10) 
                ContextDataJSON={"id": "---",
                                "type": "----",
                                "marca": {
                                "value": "---",
                                "type": "String"
                                },
                                "producto": {
                                "value": "---",
                                "type": "String"
                                },
                                "tipo":{
                                "value": "modelo",
                                "type": "String"
                                }
                                }
                ContextDataJSON['id']=str(nombre_producto)
                ContextDataJSON['type']='modelo'  
                
                ContextDataJSON['marca']['value']=marca 
                ContextDataJSON['producto']['value']=producto

                
                ContextDataJSON['tipo']['value']='modelo' # Para filtrar datos desde fiware orion
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                headers={"Accept":"application/json"}
                response= requests.post(url,headers=headers,json=ContextDataJSON) 
                # print(response.status_code)
                if (response.status_code) == 201:
                        return "El modelo ha sido creado"
                if (response.status_code) == 422:
                        return "El modelo ya existe"
                
                return "El modelo NO ha sido creado"
        except:
            return "El modelo NO ha sido creado"
# Consulta todos los modelos
def consulta_modelos_todos(paginado,offset,atributo,valor):
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        if (response.status_code==200):
            try:
                rh = json.dumps(response.headers.__dict__['_store'])
                response_JSON=json.loads(rh)
                total_id=int(response_JSON['fiware-total-count'][1])
                if (total_id!=0):    
                    dict_entidades=response.content.decode("utf-8").replace("'", '"')
                    dict_entidades=json.loads(dict_entidades)
                    while(total_id>len(dict_entidades)):
                        # print("hace")
                        # offset_aux=len(dict_entidades)+offset_aux
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(len(dict_entidades))
                        headers={"Accept":"application/json"}
                        response=requests.get(url,headers=headers)
                        # print(response)
                        dict_entidades_aux=response.content.decode("utf-8").replace("'", '"')
                        dict_entidades_aux=json.loads(dict_entidades_aux)
                        dict_entidades=dict_entidades+dict_entidades_aux
                        
                        # print(len(dict_entidades))
                        
                    for enity in dict_entidades:
                        # Reemplazamos los caracteres prohibidos para las entidades
                        enity['id']=enity['id'].replace('*', '/', 10)
                        enity['id']=enity['id'].replace('_', ' ', 10) 
                #     print(total_id)
                    return total_id,dict_entidades
                else:
                    dict_identidades=None
                    return total_id,dict_identidades
                    
            except:
                dict_identidades=None
                total_id=0
                return total_id,dict_identidades
            
        else:
            dict_identidades=None
            total_id=0
            return total_id,dict_identidades 
    except:
        dict_identidades=None
        total_id=0
        return total_id,dict_identidades

# Consulta todos los servicios sin asignar
def consulta_servicios_sin_asignar(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3,atributo_4,valor_4):
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    if (valor_3==''):
        if (valor_4!='Colombia'):
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+';'+atributo_4+'=='+valor_4+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
        else:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
    else:
        if (valor_4!='Colombia'):
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+';'+atributo_3+'~='+valor_3+';'+atributo_4+'=='+valor_4+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
        else:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+';'+atributo_3+'~='+valor_3+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        # print(response.status_code)
        if (response.status_code==200):
            try:
                rh = json.dumps(response.headers.__dict__['_store'])
                response_JSON=json.loads(rh)
                total_id=int(response_JSON['fiware-total-count'][1])
                # print(total_id)
                if (total_id!=0):    
                    dict_entidades=response.content.decode("utf-8").replace("'", '"')
                    dict_entidades=json.loads(dict_entidades)
                #     while(total_id>len(dict_entidades)):
                #         # print("hace")
                #         # offset_aux=len(dict_entidades)+offset_aux
                #         url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(len(dict_entidades))
                #         headers={"Accept":"application/json"}
                #         response=requests.get(url,headers=headers)
                #         # print(response)
                #         dict_entidades_aux=response.content.decode("utf-8").replace("'", '"')
                #         dict_entidades_aux=json.loads(dict_entidades_aux)
                #         dict_entidades=dict_entidades+dict_entidades_aux
                # #     print(dict_entidades)
                    return total_id,dict_entidades
                else:
                    dict_identidades=None
                    return total_id,dict_identidades
                   
            except:
                dict_identidades=None
                total_id=0
                return total_id,dict_identidades
            
        else:
            dict_identidades=None
            total_id=0
            return total_id,dict_identidades 
    except:
        dict_identidades=None
        total_id=0
        return total_id,dict_identidades

@login_required(redirect_field_name="")
def crear_servicio(request):
        try:
                # Crea servicio
                # Carga lista de ciudades para crear el servicio
                # Extraemos el perfil
                u=models.UserProfile.objects.get(user__username=str(request.user.username))
                # if u.cambio_ciudad==True:
                        # lista=models.UserProfile.lugar_lista # Va por la lista de ciudad del MOdels usuarios
                        # innerHtml='<option value="" disabled selected hidden>Sede</option>'                        
                        # for i in range(0,len(lista)-1):                                 
                        #                 innerHtml=innerHtml+ '<option  value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'                                                      
                        # context= {
                        #         'lista_ciudades':innerHtml ,
                        #         }
                        # return render(request, 'pages/crear_servicio.html', context) 
                # else: 
                if u.lugar!='Colombia': 
                        context= {
                                'lista_ciudades':'<option  value="'+str(u.lugar)+'">'+str(u.lugar)+'</option>'  ,
                                }
                else:
                        context= {
                                'lista_ciudades':'<option  value="'+''+'">'+'Sede inválida'+'</option>'  ,
                                }
                return render(request, 'pages/crear_servicio.html', context)
                 
        except:
                context={
                        'lista_ciudades':'',
                        }
                return render(request, 'pages/crear_servicio.html', context)
               




# @login_required(redirect_field_name="")
def lista_modelos(request):
        # Crea lista de todos los modelos                               
        if request.method == 'GET':
                try:    
                        total_id,dict_identidades=consulta_modelos_todos(1000,0,'tipo','modelo')
                        innerHtml=""
                        for i in range(0,len(dict_identidades)):
                               innerHtml=innerHtml+"<option value='"+dict_identidades[i]['id']+"'>"  
                                # innerHtml=""    
                        return JsonResponse(innerHtml,  safe=False)
                except:
                        return JsonResponse({''},  safe=False)

@login_required(redirect_field_name="")
def search_cliente(request):
        # Busca una entidad                            
        if request.method == 'GET':
                try:    
                        search_cliente = request.GET.get('search',"") 
                        dict_entity=consulta_entidad(str(search_cliente))
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        if u.lugar!='Colombia':
                                if u.lugar==dict_entity['departamento']['value']:
                                        return JsonResponse(dict_entity,  safe=False)
                                else:
                                        return JsonResponse('None',  safe=False)
                        else:
                                return JsonResponse(dict_entity,  safe=False)
                except:
                        return JsonResponse('None',  safe=False)

@login_required(redirect_field_name="")  
def search_modelo(request):
        # Busca un modelo                            
        if request.method == 'GET':
                try:    
                        search_modelo = request.GET.get('search',"")
                        # search_modelo="ERTN41L3CQI" 
                        dict_entity=consulta_modelo(str(search_modelo))
                        return JsonResponse(dict_entity,  safe=False)
                except:
                        return JsonResponse(None,  safe=False)

@login_required(redirect_field_name="")                 
def crear_cliente(request):
        # Busca un modelo                            
        if request.method == 'GET':
                try:    
                        tipo_contacto = request.GET.get('tipo_contacto',"")
                        tipo_identidad = request.GET.get('tipo_identidad',"")
                        identidad = request.GET.get('identidad',"")
                        nombre = request.GET.get('nombre',"")
                        direccion = request.GET.get('direccion',"")
                        telefono = request.GET.get('telefono',"")
                        # departamento = request.GET.get('departamento',"")
                        localidad = request.GET.get('localidad',"")
                        email = request.GET.get('email',"")
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        # if u.cambio_ciudad==True:
                        #         sede = request.GET.get('sede',"")
                        # else:
                        #         sede=str(u.lugar)
                        departamento=str(u.lugar)  # Está relacionado con la sede                
                        message=crea_contacto(tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email)
                        return JsonResponse(message,  safe=False)
                except:
                        return JsonResponse(None,  safe=False)

@login_required(redirect_field_name="")              
def crear_modelo(request):
        # Busca un modelo                            
        if request.method == 'GET':
                try:    
                        marca = request.GET.get('marca',"")
                        producto = request.GET.get('producto',"")
                        nombre_producto = request.GET.get('nombre_producto',"")
                        # print(marca,producto,nombre_producto)

                        message=crea_modelo(marca, producto, nombre_producto)
                        return JsonResponse(message,  safe=False)
                except:
                        return JsonResponse(None,  safe=False)

@login_required(redirect_field_name="")                  
def buscar_clientes(request):
        # Busca un modelo                            
        if request.method == 'GET':
                try:    
                        search_clientes = request.GET.get('search_clientes',"")
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")
                        total_enity,dict_entity=consulta_entiti_atributo(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo_contacto','Cliente','departamento',str(request.user.userprofile.lugar),'identidad',str(search_clientes))
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_entiti_atributo(int(por_pagina),0,'tipo_contacto','Cliente','departamento',str(request.user.userprofile.lugar),'identidad',str(search_clientes))
                                actual_page=1
                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        ClientesInner=""
                        for i in range(0,len(dict_entity)):
                               ClientesInner=ClientesInner+ '<tr class="filas_tabla"><td class="th1">'+str(dict_entity[i]['identidad']['value'])+'</td><td class="th2">'+str(dict_entity[i]['nombre']['value'])+'</td><td class="th3_R"><ion-icon class="select_cliente" name="checkmark-done-outline" onclick="asignar_cliente('+str(dict_entity[i])+')"></ion-icon></td></tr>'                   
                        context= {
                                'inner':ClientesInner,
                                'actual_page' : actual_page,
                                'num_pages' : num_pages,
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'inner':"",
                                'actual_page' : "actual_page",
                                'num_pages' : "num_pages",
                        }
                        return JsonResponse(context)

@login_required(redirect_field_name="")
def crear_nuevo_servicio(request):
        # Crea un servicio
    if request.user.is_superuser:                          
        if request.method == 'GET':
                try:    
                        tipo_servicio = request.GET.get('tipo_servicio',"")
                        lugar = request.GET.get('lugar',"")
                        seguimiento = request.GET.get('seguimiento',"")
                        identidad = request.GET.get('identidad',"")
                        nombre = request.GET.get('nombre',"")
                        direccion = request.GET.get('direccion',"")

                        email = request.GET.get('email',"")
                        localidad = request.GET.get('localidad',"")
                        telefono = request.GET.get('telefono',"")

                        modelo = request.GET.get('modelo',"")
                        marca = request.GET.get('marca',"")
                        producto = request.GET.get('producto',"")
                        serie = request.GET.get('serie',"")
                        doc_ref = request.GET.get('doc_ref',"")
                        falla = request.GET.get('falla',"")
                        accesorios = request.GET.get('accesorios',"")
                        observacion = request.GET.get('observacion',"")
                        asignar = request.GET.get('asignar',"0")
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        # if u.cambio_ciudad==True:
                        #         sede = request.GET.get('sede',"")
                        # else:
                        #         sede=str(u.lugar)
                        sede=str(u.lugar)

                        message=crea_servicio(tipo_servicio, lugar, seguimiento, identidad,nombre, direccion,email, localidad, telefono, modelo, marca, producto, serie,doc_ref,falla,accesorios,observacion,int(asignar),sede)
                        context= {
                                'message':message,
                        }
                        return JsonResponse(context)
                except:
                        return JsonResponse(None,  safe=False)
    else:
        context= {
                'message':'El usuario no tiene los permisos para realizar esta acción.',
        }
        return JsonResponse(context)


@login_required(redirect_field_name="")   
def buscar_servicios_filtro(request):
        # Busca todos los servicios sin asignar                                                     
        if request.method == 'GET':
                try:    
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")

                        asigna = request.GET.get('asigna',"")  
                        atributo = request.GET.get('atributo',"")
                        search = request.GET.get('search',"")
                        # print(atributo,search)
                        # acá
                        total_enity,dict_entity=consulta_servicios_sin_asignar(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo','servicio','asignar',asigna,atributo,search,'sede',str(request.user.userprofile.lugar))
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_servicios_sin_asignar(int(por_pagina),0,'tipo','servicio','asignar',asigna,atributo,search,'sede',str(request.user.userprofile.lugar))
                                actual_page=1

                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        innerHtml=""
                        for i in range(0,len(dict_entity)):
                                # Contiene asignar técnico
                                # innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1_servicios">'+str(dict_entity[i]['id'])+'</td>'  + '<td class="th2_servicios">'+str(dict_entity[i]['tipo_servicio']['value'])+'</td>' + '<td class="th3_servicios">'+str(dict_entity[i]['producto']['value'])+'</td>' + '<td class="th4_servicios">'+str(dict_entity[i]['marca']['value'])+'</td>' + '<td class="th5_servicios">'+str(dict_entity[i]['nombre']['value'])+'</td>' + '<td class="th6_servicios">'+str(dict_entity[i]['direccion']['value'])+'</td>' + '<td class="th7_servicios"> <ion-icon class="select_cliente" name="accessibility-outline" onclick="openmodal_asignar_tecnico('+str(dict_entity[i])+')"></ion-icon> <ion-icon class="select_cliente" name="eye-outline" onclick="ver_servicio('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'
                                # Sin asignar ténico                  
                                innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1_servicios">'+str(dict_entity[i]['id'])+'</td>'  + '<td class="th2_servicios">'+str(dict_entity[i]['tipo_servicio']['value'])+'</td>' + '<td class="th3_servicios">'+str(dict_entity[i]['producto']['value'])+'</td>' + '<td class="th4_servicios">'+str(dict_entity[i]['marca']['value'])+'</td>' + '<td class="th5_servicios">'+str(dict_entity[i]['nombre']['value'])+'</td>' + '<td class="th6_servicios">'+str(dict_entity[i]['direccion']['value'])+'</td>' + '<td class="th7_servicios">  <ion-icon class="select_cliente" name="eye-outline" onclick="ver_servicio('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>' 
                        context= {
                                'inner':innerHtml,
                                'actual_page' : actual_page,
                                'num_pages' : num_pages,
                        }
                        return JsonResponse(context,  safe=False)
                except:
                        context= {
                                'inner':'',
                                'actual_page' : '0',
                                'num_pages' : '0',
                        }
                        return JsonResponse(context,  safe=False)

@login_required(redirect_field_name="")            
def lista_tecnicos(request):                                                  
        if request.method == 'GET':
                try:    
                        User = get_user_model()
                        users = User.objects.all()
                        innerHtml=""
                        # Extraemos el perfil
                        user=models.UserProfile.objects.get(user__username=str(request.user.username))
                        for i in range(0,len(users)):
                                u=User.objects.get(username=str(users[i]))
                                if user.lugar!='Colombia':
                                        if (u.userprofile.rol=='3') and (u.userprofile.realiza_servicio== True) and (u.userprofile.lugar== user.lugar):  # 3 es técnico                                       
                                                innerHtml=innerHtml+ '<option value="'+str(users[i].username)+'">'+str(users[i].get_full_name())+'</option>'                                                      
                                else:
                                        if (u.userprofile.rol=='3') and (u.userprofile.realiza_servicio== True):  # 3 es técnico                                       
                                                innerHtml=innerHtml+ '<option value="'+str(users[i].username)+'">'+str(users[i].get_full_name())+'</option>'                                                      
                        context= {
                                'inner':innerHtml,
                        }
                        return JsonResponse(context,  safe=False)
                except:
                        return JsonResponse({''},  safe=False)

# Crea una lista de estados          
def lista_estados():                                                  
                try:    
                        innerHtml=' '
                        lista_estados=config.config.lista_estados
                        for i in range(0,len(lista_estados)):                                    
                                innerHtml=innerHtml+ '<option value="'+str(lista_estados[i])+'">'+str(lista_estados[i])+'</option>'                                                     
                        print(innerHtml)                           
                        return innerHtml
                except:
                        return ' '

# Esta función solo lista técnicos disponobles en la sede donde se encuentra registrado el servicio 
@login_required(redirect_field_name="")            
def lista_tecnicos_lugar(request):                                                  
        if request.method == 'GET':
                try:    
                        servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio))
                        lugar=servicio_entidad['sede']['value']        # Extraemos en qué sede se registró el servicio
                        print(lugar)
                        User = get_user_model()
                        users = User.objects.all()
                        innerHtml=""
                        for i in range(0,len(users)):
                                u=User.objects.get(username=str(users[i]))
                                if (u.userprofile.rol=='3') and (u.userprofile.realiza_servicio== True) and (u.userprofile.lugar==lugar):  # 3 es técnico                                       
                                                innerHtml=innerHtml+ '<option value="'+str(users[i].username)+'">'+str(users[i].get_full_name())+'</option>'                                                                                                          
                        context= {
                                'inner':innerHtml,
                        }
                        return JsonResponse(context,  safe=False)
                except:
                        return JsonResponse({''},  safe=False)

@login_required(redirect_field_name="")
def asigna_tecnico(request):
        # Asigna técnico                                               
        if request.method == 'GET':
                try:    
                        entity = request.GET.get('entity',"")
                        nombre = request.GET.get('nombre',"")
                        user = request.GET.get('user',"")
                        # print(user)
                        # print(type(user))
                        User = get_user_model()
                        u=User.objects.get(username=user)  # Va por los objetos del usuario con el nombre
                        nombre=u.get_full_name()
                        # status_append='Técnico asignado, debe asignar un estado'
                        # print(nombre)
                        # index=0
                        # status_append=append_attrs(entity,"tecnico_"+str(index),nombre,user)
                        status_append=update_tecnico(entity,nombre)
                        if status_append=="El técnico fue asignado":
                                update_asignar(str(entity),0) 
                                #Mensaje de asignación de técnico
                                # Crea mensaje
                                # message,id_mensaje=crea_entidad_mensaje(entity,'Asigna técnico ' + nombre,'usuario' )
                                # # print(message)
                                # if message=='ok': # Retorna ok si el mensaje fue creado                         
                                #         # Anexa el id del mensaje a la orden 
                                #         message=update_mensaje_servicio(str(entity),'mensajes',id_mensaje)
                                        

                                                       
                        # while(status_append=="no"):
                        #        index=index+1   
                        # #        status_append=append_attrs(entity,"tecnico_"+str(index),nombre,user) 
                        #        status_append=update_tecnico(entity,nombre)
                        #        if status_append=="El técnico fue asignado":
                        #               update_asignar(str(entity),1)
                        #        time.sleep(0.2)                                                                                  
                        context= {
                                'message':status_append,
                                # 'message':'Técnico asignado, debe crear un estado',
                        }
                        return JsonResponse(context,  safe=False)
                except:
                        status_append="Error en la función asinga_tecnico"
                        context= {
                                'message':status_append,
                        }
                        return JsonResponse(context,  safe=False)

@login_required(redirect_field_name="") #*#
def elimina_estado(request):
        # Elimina estado                                               
        if request.method == 'GET':
                try:    
                    servicio = request.GET.get('servicio',"")
                    id_estado = request.GET.get('id_estado',"")                       
                    usuario=request.user.username
                    servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                    sede=servicio_entidad['sede']['value']
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia': 
                        status_append=update_estado_elimina(servicio,'estados_historial',id_estado)
                        if status_append=="El estado fue desvinculado con la orden de servicio":
                                message,id_mensaje=crea_entidad_mensaje(servicio,'Elimina estado '+str(id_estado) ,'usuario' )
                                if message=='ok':                      
                                        message=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)                                                                               
                        context= {
                                'message':status_append + ' ' + id_estado,
                        }
                        return JsonResponse(context,  safe=False)
                    else:
                        context= {
                                'message':'La ciudad de sede del usuario no corresponde a la sede de la orden.',
                        }
                        return JsonResponse(context,  safe=False)
                           
                except:
                        status_append="Error en la función elimina_estado"
                        context= {
                                'message':status_append,
                        }
                        return JsonResponse(context,  safe=False)

@login_required(redirect_field_name="")
def crea_estado(request):
        # Asigna estado                                               
        if request.method == 'GET':
                try:
                    servicio = request.GET.get('servicio',"")
                    fecha_estado = str(datetime.date.today())
                    tecnico = request.GET.get('tecnico',"")
                    estado = request.GET.get('estado',"")
                    # usuario = request.GET.get('usuario',"sertek_1")   pppppp
                    usuario=request.user.username
                    servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                    sede=servicio_entidad['sede']['value']
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia': 
                        status_append,id_estado=crea_entidad_estado(servicio,fecha_estado,tecnico,estado,usuario,sede)
                        if status_append=="ok":
                                # Actualiza asignar 1 ya que tiene como mínimo un estado asignado
                                update_asignar(str(servicio),1) 
                                message,id_mensaje=crea_entidad_mensaje(servicio,'Crea estado '+str(estado)+' Técnico '+ tecnico + ' ' + id_estado ,usuario )
                                if message=='ok': # Retorna ok si el mensaje fue creado                         
                                        message=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                                        print(message)                                                                             
                        context= {
                                'message':'El estado fue creado satisfactoriamente' + ' ' + id_estado,
                        }
                        return JsonResponse(context,  safe=False)
                    else:
                        context= {
                                'message':'La ciudad de sede del usuario no corresponde a la sede de la orden.',
                        }
                        return JsonResponse(context,  safe=False)
                            
                except:
                        status_append="Error en la función crea_estado"
                        context= {
                                'message':status_append,
                        }
                        return JsonResponse(context,  safe=False)

def crea_html_remision(partes_string):
        try:
                # forma de array
                # Nombre 0, referencia 1, fecha de solcitud 2, cantidad 3, precio de venta 4, total 5, descuento 6
                # print(partes_string)
                partes_string=partes_string.split('divisor_item')
                # print(partes_string)
                html_partes=''
                for i in range(0,len(partes_string)-1):
                        print(partes_string[i])
                        partes_string_aux=partes_string[i].split(',')
                        # print(partes_string_aux)
                        html_partes=html_partes+"""
                                <div style="display: flex;">
                                <div class="info_casilla" style="width: 20%;">
                                        <div>
                                        <span>Referencia</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[1]) +"""</span>                                    
                                        </div>
                                </div>
                                <div class="info_casilla" style="width: 45%;">
                                        <div>
                                        <span>Nombre</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[0])+"""</span>
                                        </div>
                                </div>
                                <div class="info_casilla" style="width: 10%;">
                                        <div>
                                        <span>V/unitario</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[4])+"""</span>
                                        </div>
                                </div>
                                <div class="info_casilla" style="width: 5%;">
                                        <div>
                                        <span>Cantidad</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[3])+"""</span>
                                        </div>
                                </div>
                                <div class="info_casilla" style="width: 10%;">
                                        <div>
                                        <span>Descuento %</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[6])+"""</span>
                                        </div>
                                </div>
                                <div class="info_casilla" style="width: 10%;">
                                        <div>
                                        <span>Valor total</span>
                                        </div>
                                        <div>
                                        <span>"""+ str(partes_string_aux[5])+"""</span>
                                        </div>
                                </div>
                                </div>                           
                                        """
                # print(html_partes)
                return html_partes
        except:
                return ''

@login_required(redirect_field_name="")    
def elimina_remision(request):  # Elimina de la solicitud pero la remisión sigue exsitiendo como entidad
    if request.user.is_superuser:
        try:    
                # Debe iniactivar la remisión poniendo el atributo de remision activa en 0
                servicio = request.GET.get('servicio',"")   
                id_remision = request.GET.get('id_remision',"")   
                # Solicita nombre de la remision para inactivarla
                entidad_servicio=consulta_entidad(str(servicio))
                try:
                        # entidad_servicio=consulta_entidad(str(servicio))
                        if id_remision=='':
                                remision_nombre=entidad_servicio['remision']['value']
                        else:
                                remision_nombre=str(id_remision)                        
                        # Actualizamos el campo activo de la remisión
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+remision_nombre+'/attrs/'+'activa'+'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json=0)
                        if (response.status_code) == 204:
                                message_1="La remisión fue deshabilitada"
                        else :
                                message_1="La remisión NO fue deshabilitada"
                except:
                        message_1="La remisión NO fue deshabilitada"

                # print('primera parte')

                if id_remision=='' or id_remision==entidad_servicio['remision']['value']:            
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(servicio)+'/attrs/'+'remision'+'/value'
                        headers={"Content-Type":"text/plain"}        
                        response=requests.put(url,headers=headers,json='')  # Limpia los campos
                        # print(response.status_code)
                        if (response.status_code) == 204:
                                # Crea mensaje  kkkkkkk
                                message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Elimina remisión: '+ str(remision_nombre),str(request.user.username) )
                                # print(message)
                                if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                        # Anexa el id del mensaje a la orden 
                                        message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                                
                                context={
                                        'message':message_1+", La remisión fue desvinculada de la orden de servicio,"+ str(message_mensaje),
                                        }
                                return JsonResponse(context,  safe=False)
                        else :
                                context={
                                        'message': message_1+", La remisión NO fue desvinculada de la orden de servicio",
                                        }
                                return JsonResponse(context,  safe=False)
                else:
                        context={
                                'message': message_1+", La remisión NO está vinculada a una orden de servicio",
                                }
                        return JsonResponse(context,  safe=False)
                       
        except:
                context={
                        'message':"La remisión NO fue desvinculada de la orden de servicio, error en  elimina_remision",
                        }
                return JsonResponse(context,  safe=False)
    else:
                context= {
                        'message':"No tiene los permisos para realizar esta acción",
                }
                return JsonResponse(context)
    
@login_required(redirect_field_name="")
def ver_servicio(request):
        try:
                # Ver servicio                
                if request.method == 'GET':
                    servicio = request.GET.get('servicio',"")
                    servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad

                    #Evaluamos que el servicio se encuentre en la misma ciudad de quién la quiere observar
                    #FFFFFF
                    sede=servicio_entidad['sede']['value']
                    # Extraemos el perfil
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia':                           
                        #Calculamos el valor de los abonos
                        abonos=servicio_entidad['abonos']['value']
                        abonos=abonos.split(',')
                        total_abonos=0
                        for i in range(1,len(abonos)):                          
                               total_abonos=total_abonos+int(consulta_entidad(abonos[i])['valor_abono']['value'])
                        # Cargamos los mensajes ligados a la orden de servicio
                        mensajes=servicio_entidad['mensajes']['value']
                        # print(mensajes)
                        mensajes=mensajes.split(',')
                        mensajes_html=''
                        for i in range(1,len(mensajes)): 
                        #        # Creamos HTML 
                                mensaje_entidad=consulta_entidad(mensajes[i])  
                                mensaje=str(mensaje_entidad['mensaje']['value'])  
                                usuario=str(mensaje_entidad['usuario']['value'])  
                                fecha_mensaje=str(mensaje_entidad['fecha_mensaje']['value']) 

                                fecha_mensaje=fecha_mensaje.split('.')[0]
                                fecha_mensaje=fecha_mensaje.replace('T',' ')
                                mensajes_html=mensajes_html+'<div style="background-color: rgb(243, 243, 255) ;margin: 5px; padding: 5px; border-radius: 10px;"> <div><span style="font-size: small;"> '+fecha_mensaje+' </span> </div><div><span style="color: rgb(0, 13, 158); font-size: large;" > '+usuario+' </span> <span> '+mensaje+'</span></div></div>'
                                # print(mensajes[i])  
                                # mensajes_html= mensajes_html+''                   

                        # Cargamos las solicitudes de parte ligadas a la orden
                        solicitud_parte=servicio_entidad['solicitud_parte']['value']
                        solicitud_parte=solicitud_parte.split(',')
                        solicitud_parte_html=''
                        # print(solicitud_parte)
                        for i in range(1,len(solicitud_parte)): 
                        # for i in range(1,2): 
                        # #        # Creamos HTML 
                                solicitud_parte_entidad=consulta_entidad(solicitud_parte[i])  
                                # print(solicitud_parte_entidad['id'])
                                nombre_parte=str(solicitud_parte_entidad['nombre_parte']['value'])  
                                referencia=str(solicitud_parte_entidad['referencia']['value'])
                                cantidad=str(solicitud_parte_entidad['cantidad']['value'])
                                precio=str(solicitud_parte_entidad['precio']['value'])
                                total=int(precio)*int(cantidad)

                                fecha_solicitud=str(solicitud_parte_entidad['fecha_solicitud']['value']) 
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('.')[0]
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('T')[0]
                                # print(fecha_solicitud)

                                solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1_servicios">'+str(nombre_parte)+'</td><td class="th2_servicios">'+str(referencia)+'</td><td class="th3_servicios">'+str(fecha_solicitud)+'</td> <td class="th4_servicios">'+str(cantidad)+'</td> <td class="th5_servicios">'+str(precio)+'</td> <td class="th6_servicios">'+str(total)+'</td> <td class="th7_servicios">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_solicitud_parte('+"'"+str(servicio)+"'"+','+"'"+str(nombre_parte)+"'"+','+"'"+str(referencia)+"'"+','+"'"+str(fecha_solicitud)+"'"+','+"'"+str(cantidad)+"'"+','+"'"+str(precio)+"'"+','+"'"+str(total)+"'"+','+"'"+str(solicitud_parte[i])+"'"+')"></ion-icon>'+'</td> </tr>'                   
                        # print(solicitud_parte_html)
                        # Evaluamos si existe remision

                        # Cargamos los estado ligados a la orden de servicio
                        lista_estado=servicio_entidad['estados_historial']['value']
                        lista_estado=lista_estado.split(',')
                        lista_estado_html=''
                        for i in range(1,len(lista_estado)): 
                        # for i in range(1,2): 
                        # #        # Creamos HTML 
                                # aaaaaaaaa
                                estado_entidad=consulta_entidad(lista_estado[i])  
                                # print(solicitud_parte_entidad['id'])
                                fecha_estado=str(estado_entidad['fecha_estado']['value'].split('T')[0])  
                                tecnico=str(estado_entidad['tecnico']['value'])
                                estado=str(estado_entidad['estado']['value'])
                                usuario=str(estado_entidad['usuario']['value'])
                                # estado=str(estado_entidad['precio']['value'])
                                # total=int(precio)*int(cantidad)

                                # fecha_solicitud=str(solicitud_parte_entidad['fecha_solicitud']['value']) 
                                # print(fecha_solicitud)
                                # fecha_solicitud=fecha_solicitud.split('.')[0]
                                # print(fecha_solicitud)
                                # fecha_solicitud=fecha_solicitud.split('T')[0]
                                # print(fecha_solicitud)

                                lista_estado_html=lista_estado_html+'<tr class="filas_tabla"><td class="th1_estado">'+str(fecha_estado)+'</td><td class="th2_estado">'+str(tecnico)+'</td><td class="th3_estado">'+str(estado)+'</td><td class="th4_estado">'+str(usuario)+'</td>  <td class="th5_estado">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_estado('+ str(estado_entidad) +')"></ion-icon>'+'</td> </tr>'                   

                        try:
                                if (servicio_entidad['remision']['value'] !=''):
                                        # Existe remisión
                                        texto_boton_remision='Ver remisión'
                                        # print(servicio_entidad['remision']['value'])

                                        entidad_remision=consulta_entidad(servicio_entidad['remision']['value']) # Va por la entidad
                                                # print(entidad_remision)
                                        # print(entidad_remision)
                                        
                                        # Vamos por total remision
                                        # total_remision='123'
                                        try:
                                                total_remision=entidad_remision['total']['value']
                                                funcion_boton_remision='ver_remision_existente()'
                                                # Creamos HTML de las partes
                                                hmtl_partes=crea_html_remision(entidad_remision['informacion_parte']['value'])

                                                context={
                                                        'servicio':servicio_entidad['id'],
                                                        'fecha_de_creacion':servicio_entidad['fecha']['value'].split('T')[0],
                                                        'lugar':servicio_entidad['lugar']['value'],
                                                        'tipo_de_servicio':servicio_entidad['tipo_servicio']['value'],
                                                        'seguimiento':servicio_entidad['seguimiento']['value'],
                                                        # Asigna el último técnico  tecnico_X  
                                                        'tecnico':servicio_entidad['tecnico']['value'],  #  ******* Poner último técnico asignado
                                                        'nombre':servicio_entidad['nombre']['value'],
                                                        'identidad':servicio_entidad['identidad']['value'],
                                                        'direccion':servicio_entidad['direccion']['value'],
                                                        'localidad':servicio_entidad['localidad']['value'],  #***** Agregar localidad
                                                        'telefono':servicio_entidad['telefono']['value'],    #***** Agregar telefono
                                                        'email':servicio_entidad['email']['value'],      #***** Agregar email
                                                        'marca':servicio_entidad['marca']['value'],
                                                        'producto':servicio_entidad['producto']['value'],
                                                        'modelo':servicio_entidad['modelo']['value'],
                                                        'serie':servicio_entidad['serie']['value'],
                                                        'doc_ref':servicio_entidad['doc_ref']['value'],
                                                        'falla':servicio_entidad['falla']['value'],
                                                        'accesorios':servicio_entidad['accesorios']['value'],
                                                        'observacion':servicio_entidad['observacion']['value'],
                                                        # 
                                                        'estado':urllib.parse.unquote(servicio_entidad['estado']['value']),
                                                        'fecha_de_estado':servicio_entidad['fecha_estado']['value'].split('T')[0],

                                                        # 'total_abonos': total_abonos,
                                                        'total_abonos': f"{total_abonos:,}",
                                                        'informacion_parte_tabla': solicitud_parte_html,
                                                        'notas':mensajes_html,
                                                        # Esto es de la remisión
                                                        'texto_boton_remision':texto_boton_remision,
                                                        'total_remision':total_remision,
                                                        'funcion_boton_remision':funcion_boton_remision,
                                                        # Ver remision
                                                        # servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte):
                                                        'forma_pago_ver_remision':entidad_remision['forma_pago']['value'],
                                                        'medio_pago_ver_remision':entidad_remision['medio_pago']['value'],
                                                        'fecha_vencimiento_ver_remision':entidad_remision['fecha_vencimiento']['value'].split('T')[0],
                                                        'servicio_ver_remision':entidad_remision['servicio']['value'],
                                                        'producto_ver_remision':entidad_remision['producto']['value'],
                                                        'marca_ver_remision':entidad_remision['marca']['value'],
                                                        'identidad_ver_remision':entidad_remision['identificacion']['value'],
                                                        'nombre_ver_remision':entidad_remision['cliente']['value'],
                                                        'direccion_ver_remision':entidad_remision['direccion']['value'],
                                                        'total_abonos_ver_remision':entidad_remision['total_abonos']['value'],
                                                        'subtotal_ver_remision':entidad_remision['subtotal']['value'],
                                                        'descuento_ver_remision':entidad_remision['descuento']['value'],
                                                        'total_ver_remision':entidad_remision['total']['value'],  
                                                        'usuario_ver_remision':entidad_remision['usuario']['value'],                                
                                                        'informacion_parte_ver_remision':entidad_remision['informacion_parte']['value'],         
                                                        'informacion_parte_ver_remision':hmtl_partes, 
                                                        'informacion_estados_tabla':  lista_estado_html,
                                                        'lista_estados_tabla':lista_estados(),           
                                                        }
                                        except:
                                                texto_boton_remision='Generar remisión'
                                                funcion_boton_remision='load_remision()'
                                                total_remision='$ 0'
                                                context={
                                                        
                                                        'servicio':servicio_entidad['id'],
                                                        'fecha_de_creacion':servicio_entidad['fecha']['value'].split('T')[0],
                                                        'lugar':servicio_entidad['lugar']['value'],
                                                        'tipo_de_servicio':servicio_entidad['tipo_servicio']['value'],
                                                        'seguimiento':servicio_entidad['seguimiento']['value'],
                                                        # Asigna el último técnico  tecnico_X  
                                                        'tecnico':servicio_entidad['tecnico']['value'],  #  ******* Poner último técnico asignado
                                                        'nombre':servicio_entidad['nombre']['value'],
                                                        'identidad':servicio_entidad['identidad']['value'],
                                                        'direccion':servicio_entidad['direccion']['value'],
                                                        'localidad':servicio_entidad['localidad']['value'],  #***** Agregar localidad
                                                        'telefono':servicio_entidad['telefono']['value'],    #***** Agregar telefono
                                                        'email':servicio_entidad['email']['value'],      #***** Agregar email
                                                        'marca':servicio_entidad['marca']['value'],
                                                        'producto':servicio_entidad['producto']['value'],
                                                        'modelo':servicio_entidad['modelo']['value'],
                                                        'serie':servicio_entidad['serie']['value'],
                                                        'doc_ref':servicio_entidad['doc_ref']['value'],
                                                        'falla':servicio_entidad['falla']['value'],
                                                        'accesorios':servicio_entidad['accesorios']['value'],
                                                        'observacion':servicio_entidad['observacion']['value'],
                                                        # 
                                                        # 'estado':urllib.parse.unquote(servicio_entidad['estado']['value']),
                                                        # 'estado':servicio_entidad['estado']['value'],
                                                        'estado':urllib.parse.unquote(servicio_entidad['estado']['value']),
                                                        'fecha_de_estado':servicio_entidad['fecha_estado']['value'].split('T')[0],
                                                        # 'total_abonos': total_abonos,
                                                        'total_abonos': f"{total_abonos:,}",
                                                        'informacion_parte_tabla': solicitud_parte_html,
                                                        'notas':mensajes_html,
                                                        # Esto es de la remisión
                                                        'texto_boton_remision':texto_boton_remision,
                                                        'total_remision':total_remision,
                                                        'funcion_boton_remision':funcion_boton_remision, 
                                                        'informacion_estados_tabla':  lista_estado_html,  
                                                        'lista_estados_tabla':lista_estados(),                 
                                                        }
                                else:
                                        texto_boton_remision='Generar remisión'
                                        funcion_boton_remision='load_remision()'
                                        total_remision='$ 0'
                                        context={
                                                'servicio':servicio_entidad['id'],
                                                'fecha_de_creacion':servicio_entidad['fecha']['value'].split('T')[0],
                                                'lugar':servicio_entidad['lugar']['value'],
                                                'tipo_de_servicio':servicio_entidad['tipo_servicio']['value'],
                                                'seguimiento':servicio_entidad['seguimiento']['value'],
                                                # Asigna el último técnico  tecnico_X  
                                                'tecnico':servicio_entidad['tecnico']['value'],  #  ******* Poner último técnico asignado
                                                'nombre':servicio_entidad['nombre']['value'],
                                                'identidad':servicio_entidad['identidad']['value'],
                                                'direccion':servicio_entidad['direccion']['value'],
                                                'localidad':servicio_entidad['localidad']['value'],  #***** Agregar localidad
                                                'telefono':servicio_entidad['telefono']['value'],    #***** Agregar telefono
                                                'email':servicio_entidad['email']['value'],      #***** Agregar email
                                                'marca':servicio_entidad['marca']['value'],
                                                'producto':servicio_entidad['producto']['value'],
                                                'modelo':servicio_entidad['modelo']['value'],
                                                'serie':servicio_entidad['serie']['value'],
                                                'doc_ref':servicio_entidad['doc_ref']['value'],
                                                'falla':servicio_entidad['falla']['value'],
                                                'accesorios':servicio_entidad['accesorios']['value'],
                                                'observacion':servicio_entidad['observacion']['value'],
                                                # 
                                                'estado':urllib.parse.unquote(servicio_entidad['estado']['value']),
                                                # 'estado':servicio_entidad['estado']['value'],-----------
                                                # 'estado':urllib.parse.unquote(servicio_entidad['estado']['value']),
                                                'fecha_de_estado':servicio_entidad['fecha_estado']['value'].split('T')[0],
                                                # 'total_abonos': total_abonos,
                                                'total_abonos': f"{total_abonos:,}",
                                                'informacion_parte_tabla': solicitud_parte_html,
                                                'informacion_estados_tabla':  lista_estado_html, 
                                                'notas':mensajes_html,
                                                # Esto es de la remisión
                                                'texto_boton_remision':texto_boton_remision,
                                                'total_remision':total_remision,
                                                'funcion_boton_remision':funcion_boton_remision,
                                                # Ver remision
                                                # servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte):
                                                # 'forma_pago_ver_remision':entidad_remision['forma_pago']['value'],
                                                # 'medio_pago_ver_remision':entidad_remision['medio_pago']['value'],
                                                # 'fecha_vencimiento_ver_remision':entidad_remision['fecha_vencimiento']['value'].split('T')[0],
                                                # 'servicio_ver_remision':entidad_remision['servicio']['value'],
                                                # 'producto_ver_remision':entidad_remision['producto']['value'],
                                                # 'marca_ver_remision':entidad_remision['marca']['value'],
                                                # 'identidad_ver_remision':entidad_remision['identificacion']['value'],
                                                # 'nombre_ver_remision':entidad_remision['cliente']['value'],
                                                # 'direccion_ver_remision':entidad_remision['direccion']['value'],
                                                # 'total_abonos_ver_remision':entidad_remision['total_abonos']['value'],
                                                # 'subtotal_ver_remision':entidad_remision['subtotal']['value'],
                                                # 'descuento_ver_remision':entidad_remision['descuento']['value'],
                                                # 'total_ver_remision':entidad_remision['total']['value'],  
                                                # 'usuario_ver_remision':entidad_remision['usuario']['value'],                                
                                                # 'informacion_parte_ver_remision':entidad_remision['informacion_parte']['value'],         
                                                # 'informacion_parte_ver_remision':hmtl_partes,  
                                                'lista_estados_tabla':lista_estados(),                 
                                                }
                        except:
                                texto_boton_remision='Generar remisión',
                                funcion_boton_remision='load_remision()',
                                total_remision='$ 0',
                                context={  
                                        'funcion_boton_remision':funcion_boton_remision,  
                                        'texto_boton_remision':texto_boton_remision,   
                                        'total_remision':total_remision,     
                                        }

                        # Generamos HTML de información parte 
                        # hmtl_partes=crea_html_remision(entidad_remision['informacion_parte']['value'])

                        # context={
                        #         'servicio':servicio_entidad['id'],
                        #         'fecha_de_creacion':servicio_entidad['fecha']['value'].split('T')[0],
                        #         'lugar':servicio_entidad['lugar']['value'],
                        #         'tipo_de_servicio':servicio_entidad['tipo_servicio']['value'],
                        #         'seguimiento':servicio_entidad['seguimiento']['value'],
                        #         # Asigna el último técnico  tecnico_X  
                        #         'tecnico':servicio_entidad['tecnico']['value'],  #  ******* Poner último técnico asignado
                        #         'nombre':servicio_entidad['nombre']['value'],
                        #         'identidad':servicio_entidad['identidad']['value'],
                        #         'direccion':servicio_entidad['direccion']['value'],
                        #         'localidad':servicio_entidad['localidad']['value'],  #***** Agregar localidad
                        #         'telefono':servicio_entidad['telefono']['value'],    #***** Agregar telefono
                        #         'email':servicio_entidad['email']['value'],      #***** Agregar email
                        #         'marca':servicio_entidad['marca']['value'],
                        #         'producto':servicio_entidad['producto']['value'],
                        #         'modelo':servicio_entidad['modelo']['value'],
                        #         'serie':servicio_entidad['serie']['value'],
                        #         'doc_ref':servicio_entidad['doc_ref']['value'],
                        #         'falla':servicio_entidad['falla']['value'],
                        #         'accesorios':servicio_entidad['accesorios']['value'],
                        #         'observacion':servicio_entidad['observacion']['value'],
                        #         # 'total_abonos': total_abonos,
                        #         'total_abonos': f"{total_abonos:,}",
                        #         'informacion_parte_tabla': solicitud_parte_html,
                        #         'notas':mensajes_html,
                        #         # Esto es de la remisión
                        #         'texto_boton_remision':texto_boton_remision,
                        #         'total_remision':total_remision,
                        #         'funcion_boton_remision':funcion_boton_remision,
                        #         # Ver remision
                        #         # servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte):
                        #         # 'forma_pago_ver_remision':entidad_remision['forma_pago']['value'],
                        #         # 'medio_pago_ver_remision':entidad_remision['medio_pago']['value'],
                        #         # 'fecha_vencimiento_ver_remision':entidad_remision['fecha_vencimiento']['value'].split('T')[0],
                        #         # 'servicio_ver_remision':entidad_remision['servicio']['value'],
                        #         # 'producto_ver_remision':entidad_remision['producto']['value'],
                        #         # 'marca_ver_remision':entidad_remision['marca']['value'],
                        #         # 'identidad_ver_remision':entidad_remision['identificacion']['value'],
                        #         # 'nombre_ver_remision':entidad_remision['cliente']['value'],
                        #         # 'direccion_ver_remision':entidad_remision['direccion']['value'],
                        #         # 'total_abonos_ver_remision':entidad_remision['total_abonos']['value'],
                        #         # 'subtotal_ver_remision':entidad_remision['subtotal']['value'],
                        #         # 'descuento_ver_remision':entidad_remision['descuento']['value'],
                        #         # 'total_ver_remision':entidad_remision['total']['value'],  
                        #         # 'usuario_ver_remision':entidad_remision['usuario']['value'],                                
                        #         # 'informacion_parte_ver_remision':entidad_remision['informacion_parte']['value'],         
                        #         # 'informacion_parte_ver_remision':hmtl_partes,                 
                        #         }
                        return render(request, 'pages/ver_servicio.html', context)
                    else:  # Si es de una ciudad diferente envía un mensaje de error
                        context={
                                }
                        return render(request, 'pages/error.html', context)
                                                  
                else:
                        context={
                                }
                        return render(request, 'pages/ver_servicio.html', context)
        except:
                context={
                        }
                return render(request, 'pages/ver_servicio.html', context)


@login_required(redirect_field_name="")        
def crea_abono(request):
        try:
                # Crea abono               
                if request.method == 'GET':
                        servicio = request.GET.get('servicio',"")  # Contiene la id del servicio
                        medio_de_pago = request.GET.get('medio_de_pago',"")
                        nombre_razon_social = request.GET.get('nombre_razon_social',"")
                        detalle = request.GET.get('detalle',"")
                        valor_abono = request.GET.get('valor_abono',"")

                        usuario=request.user.username
                        # Crea entidad de abono
                        message,id_abono=crea_entidad_abono(servicio, medio_de_pago, nombre_razon_social, detalle, valor_abono,usuario)
                  
                        if message=='ok': # Retorna ok si el abono fue creado                         
                                # Anexa el id del abono a la orden 
                                message=update_abonos_servicio(str(servicio),'abonos',id_abono)
                                # Crea mensaje 
                                message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Crea abono valor:'+ str(valor_abono) +' id:' + str(id_abono),str(request.user.username))
                                # print(message)
                                if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                        # Anexa el id del mensaje a la orden 
                                        message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)

                                # Calcula el total de abonos
                                servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                                #Calculamos el valor de los abonos
                                abonos=servicio_entidad['abonos']['value']
                                abonos=abonos.split(',')
                                total_abonos=0
                                for i in range(1,len(abonos)):                          
                                        total_abonos=total_abonos+int(consulta_entidad(abonos[i])['valor_abono']['value'])
                                        # print(message)
                        context={
                                'message':message,
                                'total_abonos':'$ '+ f"{total_abonos:,}",
                                }
                        return JsonResponse(context,  safe=False)
                else:
                        context={
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                        }
                return JsonResponse(context,  safe=False)

# actualiza cuadro de estado para evitar recargar toda la página 
@login_required(redirect_field_name="")     
def update_estado_panel(request):
        try:             # nnnnnnnn
                if request.method == 'GET':
                    servicio = request.GET.get('servicio',"") 
                    servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                    sede=servicio_entidad['sede']['value']
                    # Extraemos el perfil
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia': 
                        # Cargamos los estados ligados a la orden de servicio
                        lista_estado=servicio_entidad['estados_historial']['value']
                        lista_estado=lista_estado.split(',')
                        lista_estado_html=''
                        for i in range(1,len(lista_estado)): 
                                estado_entidad=consulta_entidad(lista_estado[i])  
                                fecha_estado=str(estado_entidad['fecha_estado']['value'].split('T')[0])  
                                tecnico=str(estado_entidad['tecnico']['value'])
                                estado=str(estado_entidad['estado']['value'])
                                usuario=str(estado_entidad['usuario']['value'])
                                lista_estado_html=lista_estado_html+'<tr class="filas_tabla"><td class="th1_estado">'+str(fecha_estado)+'</td><td class="th2_estado">'+str(tecnico)+'</td><td class="th3_estado">'+str(estado)+'</td><td class="th4_estado">'+str(usuario)+'</td>  <td class="th5_estado">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_estado('+ str(estado_entidad) +')"></ion-icon>'+'</td> </tr>'
                        context={
                                'estados_html':lista_estado_html,
                                }
                        return JsonResponse(context,  safe=False)
                    else:
                        context={
                                }
                        return JsonResponse(context,  safe=False)
                            
                else:
                        context={
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                        }
                return JsonResponse(context,  safe=False)

# actualiza cuadro de mensajes para evitar recargar toda la página 
@login_required(redirect_field_name="")     
def update_mensaje(request):
        try:
                # Crea abono               
                if request.method == 'GET':
                        servicio = request.GET.get('servicio',"")  # Contiene la id del servicio
                        # Agregamos los mensajes en html para evitar parpadeo
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        # Cargamos los mensajes ligados a la orden de servicio
                        mensajes=servicio_entidad['mensajes']['value']
                        mensajes=mensajes.split(',')
                        mensajes_html=''
                        for i in range(1,len(mensajes)): 
                                mensaje=str(consulta_entidad(mensajes[i])['mensaje']['value'])  
                                usuario=str(consulta_entidad(mensajes[i])['usuario']['value'])  
                                fecha_mensaje=str(consulta_entidad(mensajes[i])['fecha_mensaje']['value'])   
                                fecha_mensaje=fecha_mensaje.split('.')[0]
                                fecha_mensaje=fecha_mensaje.replace('T',' ')
                                mensajes_html=mensajes_html+'<div style="background-color: rgb(243, 243, 255) ;margin: 5px; padding: 5px; border-radius: 10px;"> <div><span style="font-size: small;"> '+fecha_mensaje+' </span> </div><div><span style="color: rgb(0, 13, 158); font-size: large;" > '+usuario+' </span> <span> '+mensaje+'</span></div></div>'

                        context={
                                'mensajes_html':mensajes_html,
                                }
                        return JsonResponse(context,  safe=False)
                else:
                        context={
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                        }
                return JsonResponse(context,  safe=False)

# Crea mensaje  
@login_required(redirect_field_name="")     
def crea_mensaje(request):
        try:
                # Crea abono               
                if request.method == 'GET':
                        servicio = request.GET.get('servicio',"")  # Contiene la id del servicio
                        mensaje = request.GET.get('mensaje',"")
                        # usuario = request.GET.get('usuario',"Sertek")
                        usuario=request.user.username
                        # Crea mensaje
                        message,id_mensaje=crea_entidad_mensaje(servicio, mensaje,usuario )
                        # print(message)
                        if message=='ok': # Retorna ok si el abono fue creado                         
                                # Anexa el id del abono a la orden 
                                message=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                                pass
                        # Agregamos los mensajes en html para evitar parpadeo
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        # Cargamos los mensajes ligados a la orden de servicio
                        mensajes=servicio_entidad['mensajes']['value']
                        # print(mensajes)
                        mensajes=mensajes.split(',')
                        mensajes_html=''
                        for i in range(1,len(mensajes)): 
                        #        # Creamos HTML 
                                mensaje=str(consulta_entidad(mensajes[i])['mensaje']['value'])  
                                usuario=str(consulta_entidad(mensajes[i])['usuario']['value'])  
                                fecha_mensaje=str(consulta_entidad(mensajes[i])['fecha_mensaje']['value'])   
                                fecha_mensaje=fecha_mensaje.split('.')[0]
                                fecha_mensaje=fecha_mensaje.replace('T',' ')
                                mensajes_html=mensajes_html+'<div style="background-color: rgb(243, 243, 255) ;margin: 5px; padding: 5px; border-radius: 10px;"> <div><span style="font-size: small;"> '+fecha_mensaje+' </span> </div><div><span style="color: rgb(0, 13, 158); font-size: large;" > '+usuario+' </span> <span> '+mensaje+'</span></div></div>'
                                # print(mensajes[i])  
                                # mensajes_html= mensajes_html+''                   
                                

                        # print(mensajes_html)

                        context={
                                'message':message,
                                'id_abono':id_mensaje,
                                'mensajes_html':mensajes_html,
                                }
                        return JsonResponse(context,  safe=False)
                else:
                        context={
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                        }
                return JsonResponse(context,  safe=False)
        
def lista_detalle_abonos(request):
        # Crea la lista de detalle abonos.                          
        if request.method == 'GET':
                try:    
                        servicio = request.GET.get('servicio',"")
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")
                        # Consulta los abonos ligados a una orden 
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        # Extraemos número de documento de la persona ligada a la orden de servicio
                        identidad=servicio_entidad['identidad']['value']
                        # Calculamos el valor de los abonos de servicio
                        abonos=servicio_entidad['abonos']['value']
                        abonos=abonos.split(',')
                        AbonosInner=''
                        # Generamos lista 
                        if (len(abonos)>1):
                                for i in range(1,len(abonos)):
                                        #Extramos datos de cada abono
                                        
                                        # print(identidad)
                                        abono_entidad=consulta_entidad(str(abonos[i])) # Va por la entidad
                                        abono_entidad['fecha_abono']['value']=abono_entidad['fecha_abono']['value'].split('T')[0]
                                        # print(abono_entidad)
                                        AbonosInner=AbonosInner+'<tr class="filas_tabla"><td class="th1_abonos">'+str(identidad)+'</td><td class="th2_abonos">'+str(abono_entidad['fecha_abono']['value']).split('T')[0]+'</td><td class="th3_abonos">'+str(abono_entidad['medio_de_pago']['value'])+'</td> <td class="th4_abonos">'+str(abono_entidad['detalle']['value'])+'</td> <td class="th5_abonos">'+str(abono_entidad['valor_abono']['value'])+'</td> <td class="th6_abonos">'+str(abono_entidad['usuario']['value'])+'</td> <td class="th7_abonos"><ion-icon class="list_action" name="trash-outline" onclick="eliminar_abono('+str(abono_entidad)+')"></ion-icon></td></tr>'                   
                                        
                        # print(AbonosInner)       
                        # abonos=abonos[1]
                        # total_enity,dict_entity=consulta_entiti_atributo(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo_contacto','Cliente','departamento','Bogotá','identidad',str(search_clientes))
                        # if (len(dict_entity)==0) and (actual_page!='1'):
                        #         total_enity,dict_entity=consulta_entiti_atributo(int(por_pagina),0,'tipo_contacto','Cliente','departamento','Bogotá','identidad',str(search_clientes))
                        #         actual_page=1
                        # num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        # ClientesInner=""
                        # for i in range(0,len(dict_entity)):
                        #        ClientesInner=ClientesInner+ '<tr class="filas_tabla"><td class="th1">'+str(dict_entity[i]['identidad']['value'])+'</td><td class="th2">'+str(dict_entity[i]['nombre']['value'])+'</td><td class="th3_R"><ion-icon class="select_cliente" name="checkmark-done-outline" onclick="asignar_cliente('+str(dict_entity[i])+')"></ion-icon></td></tr>'                   
                        context= {
                                'inner':AbonosInner,
                                'actual_page' : 'actual_page',
                                'num_pages' : 'num_pages',
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'inner':"",
                                'actual_page' : "actual_page",
                                'num_pages' : "num_pages",
                        }
                        return JsonResponse(context)

@login_required(redirect_field_name="")  
def lista_partes(request):
        # Crea la lista de partes.                          
        if request.method == 'GET':
                try:    
                        #ZZZZZ
                        parte = request.GET.get('parte',"")
                        parte=urllib.parse.quote(parte.upper())

                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        print(u.lugar)

                        total_id,partes_dict=consulta_partes(1000,0,'tipo','parte','referencia',str(parte),'activo',1,'ciudad',str(u.lugar))
                        print(len(partes_dict))
                        if len(partes_dict)==0:
                                total_id,partes_dict=consulta_partes(1000,0,'tipo','parte','nombre_parte',str(parte),'activo',1,'ciudad',str(u.lugar))


                        PartesInner=''
                        # if (len(partes_dict)>0):
                        for i in range(0,len(partes_dict)):
                                PartesInner=PartesInner+'<tr class="filas_tabla"><td class="th1_sol_parte">'+str(urllib.parse.unquote(partes_dict[i]['nombre_parte']['value']))+'</td><td class="th2_sol_parte">'+str(urllib.parse.unquote(partes_dict[i]['referencia']['value']))+'</td><td class="th3_sol_parte">'+str(partes_dict[i]['cantidad']['value'])+'</td><td class="th4_sol_parte">'+str(partes_dict[i]['precio']['value'])+'</td>  <td class="th5_sol_parte"><ion-icon class="asignar_parte" name="checkmark-done-outline" onclick="asignar_parte('+"'"+str(urllib.parse.unquote(partes_dict[i]['nombre_parte']['value']))+"'"+','+"'"+str(urllib.parse.unquote(partes_dict[i]['referencia']['value']))+"'"+','+"'"+str(partes_dict[i]['precio']['value'])+"'"+','+"'"+str(partes_dict[i]['id'])+"'" +')"></ion-icon></td></tr>'                                                         
                        context= {
                                'inner':PartesInner,
                                'actual_page' : 'actual_page',
                                'num_pages' : 'num_pages',
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'inner':"",
                                'actual_page' : "actual_page",
                                'num_pages' : "num_pages",
                        }
                        return JsonResponse(context)

@login_required(redirect_field_name="")            
def crea_solicitud_parte(request):
        # Crea la lista de partes.                          
        if request.method == 'GET':
                try:    
                        servicio = request.GET.get('servicio',"")
                        nombre_parte = request.GET.get('nombre_parte',"")
                        referencia = request.GET.get('referencia',"")
                        precio = request.GET.get('precio',0)
                        cantidad = request.GET.get('cantidad',0)
                        id_parte = request.GET.get('id_parte',0)
                        # Verificamos que la cantidad solicitada sea mayor o igual existente
                        parte_entidad=consulta_entidad(str(id_parte)) # Va por la entidad
                        # print(parte_entidad['cantidad']['value'])
                        if int(parte_entidad['cantidad']['value'])<int(cantidad):
                                context= {
                                'message' : 'La cantidad solicitada no se encuentra disponible',
                                'inner': '',
                                }
                                return JsonResponse(context)

                        # usuario = request.GET.get('usuario',"")
                        usuario=request.user.username
                        message,id_entidad=crea_entidad_solicitud_parte(servicio,nombre_parte,referencia,precio,cantidad,usuario)
                        # Resta la cantidad a la existente HHHHHHHHH

                        ContextDataJSON={"cantidad": {
                        "value": int(int(parte_entidad['cantidad']['value'])-int(cantidad)),
                        "type": "integer"
                        }
                        }
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(id_parte)+'/attrs/'
                        headers={"Accept":"application/json"}      
                        response=requests.post(url,headers=headers,json=ContextDataJSON)
                        # if (response.status_code) == 204:
                        #         context={
                        #                 'message':'El mensaje fue publicado.',
                        #         }
                        #         return JsonResponse(context,  safe=False)
                        # else :
                        #         context={
                        #                 'message':'El mensaje NO fue publicado.',
                        #         }
                        #         return JsonResponse(context,  safe=False)

                        message=update_solicitud(servicio,'solicitud_parte',id_entidad)


                        

                        # Crea mensaje 
                        message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Crea parte:'+ str(referencia) +' id:' + str(id_entidad),usuario )
                        # print(message)
                        if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                # Anexa el id del mensaje a la orden 
                                message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                        
                        # Actualiza información de parte en el html
                        # Cargamos las solicitudes de parte ligadas a la orden
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        solicitud_parte=servicio_entidad['solicitud_parte']['value']
                        solicitud_parte=solicitud_parte.split(',')
                        solicitud_parte_html=''
                        # print(solicitud_parte)
                        for i in range(1,len(solicitud_parte)): 
                        # for i in range(1,2): 
                        # #        # Creamos HTML 
                                solicitud_parte_entidad=consulta_entidad(solicitud_parte[i])  
                                nombre_parte=str(solicitud_parte_entidad['nombre_parte']['value'])  
                                referencia=str(solicitud_parte_entidad['referencia']['value'])
                                cantidad=str(solicitud_parte_entidad['cantidad']['value'])
                                precio=str(solicitud_parte_entidad['precio']['value'])
                                total=int(precio)*int(cantidad)

                                fecha_solicitud=str(solicitud_parte_entidad['fecha_solicitud']['value']) 
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('.')[0]
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('T')[0]
                                # print(fecha_solicitud)

                                # solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1_servicios">'+str(nombre_parte)+'</td><td class="th2_servicios">'+str(referencia)+'</td><td class="th3_servicios">'+str(fecha_solicitud)+'</td> <td class="th4_servicios">'+str(cantidad)+'</td> <td class="th5_servicios">'+str(precio)+'</td> <td class="th6_servicios">'+str(total)+'</td> <td class="th7_servicios">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_solicitud_parte('+str(total)+')"></ion-icon>'+'</td> </tr>'                   
                                solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1_servicios">'+str(nombre_parte)+'</td><td class="th2_servicios">'+str(referencia)+'</td><td class="th3_servicios">'+str(fecha_solicitud)+'</td> <td class="th4_servicios">'+str(cantidad)+'</td> <td class="th5_servicios">'+str(precio)+'</td> <td class="th6_servicios">'+str(total)+'</td> <td class="th7_servicios">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_solicitud_parte('+"'"+str(servicio)+"'"+','+"'"+str(nombre_parte)+"'"+','+"'"+str(referencia)+"'"+','+"'"+str(fecha_solicitud)+"'"+','+"'"+str(cantidad)+"'"+','+"'"+str(precio)+"'"+','+"'"+str(total)+"'"+','+"'"+str(solicitud_parte[i])+"'"+')"></ion-icon>'+'</td> </tr>'                   
                        # print(solicitud_parte_html)

                        context= {                             
                                'message' : message,
                                'inner': solicitud_parte_html,
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'message' : 'Error en crea_solicitud_parte',
                                'inner': '',
                        }
                        return JsonResponse(context)


# Elimina la solicitud de parte de la orden de servicio. Pero no elimina la entidad creada por motivos de seguridad
@login_required(redirect_field_name="")
def elimina_solicitud_parte(request):                        
        if request.method == 'GET':
                try:    
                        
                        servicio = request.GET.get('servicio',"")
                        id_solicitud = request.GET.get('id_solicitud',"")
                        if request.user.is_superuser:
                                message=update_solicitud_elimina(str(servicio),'solicitud_parte',str(id_solicitud))
                        else:
                                message='No tiene los permisos para realizar esta acción'
                        # Crea mensaje 
                        message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Elimina parte: '+ str(id_solicitud),'usuario' )
                        # print(message)
                        if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                # Anexa el id del mensaje a la orden 
                                message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)

                        # # Vamos por la entidad de solcitud de servicio y extraemos las solicitudes de partes
                        # servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        # solicitud_parte=servicio_entidad['solicitud_parte']['value']
                        # solicitud_parte=solicitud_parte.split(',')
                        # # Comparamos con el id de la solicitud y hacemos un pop de la lista y hacemos update da del campo 'solicitud_parte' de la orden de servicio.  
                        # for i in range(1,len(solicitud_parte)): 
                        #        if (solicitud_parte[i]==id_solicitud): # Si es igual la sacamos de la lista
                        #                 solicitud_parte.pop(i)
                        # # Hacemos el update 
                              
                        
                        
                        
                        
                        
                        
                        # Actualiza información de parte
                        # Cargamos las solicitudes de parte ligadas a la orden
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        solicitud_parte=servicio_entidad['solicitud_parte']['value']
                        solicitud_parte=solicitud_parte.split(',')
                        solicitud_parte_html=''
                        # print(solicitud_parte)
                        for i in range(1,len(solicitud_parte)): 
                        # for i in range(1,2): 
                        # #        # Creamos HTML 
                                solicitud_parte_entidad=consulta_entidad(solicitud_parte[i])  
                                nombre_parte=str(solicitud_parte_entidad['nombre_parte']['value'])  
                                referencia=str(solicitud_parte_entidad['referencia']['value'])
                                cantidad=str(solicitud_parte_entidad['cantidad']['value'])
                                precio=str(solicitud_parte_entidad['precio']['value'])
                                total=int(precio)*int(cantidad)

                                fecha_solicitud=str(solicitud_parte_entidad['fecha_solicitud']['value']) 
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('.')[0]
                                # print(fecha_solicitud)
                                fecha_solicitud=fecha_solicitud.split('T')[0]
                                # print(fecha_solicitud)

                                # solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1_servicios">'+str(nombre_parte)+'</td><td class="th2_servicios">'+str(referencia)+'</td><td class="th3_servicios">'+str(fecha_solicitud)+'</td> <td class="th4_servicios">'+str(cantidad)+'</td> <td class="th5_servicios">'+str(precio)+'</td> <td class="th6_servicios">'+str(total)+'</td> <td class="th7_servicios">'+ '<ion-icon class="list_action" name="trash-outline" onclick="ver_servicio('+str(total)+')"></ion-icon>'+'</td> </tr>'                   
                                solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1_servicios">'+str(nombre_parte)+'</td><td class="th2_servicios">'+str(referencia)+'</td><td class="th3_servicios">'+str(fecha_solicitud)+'</td> <td class="th4_servicios">'+str(cantidad)+'</td> <td class="th5_servicios">'+str(precio)+'</td> <td class="th6_servicios">'+str(total)+'</td> <td class="th7_servicios">'+ '<ion-icon class="list_action" name="trash-outline" onclick="elimina_solicitud_parte('+"'"+str(servicio)+"'"+','+"'"+str(nombre_parte)+"'"+','+"'"+str(referencia)+"'"+','+"'"+str(fecha_solicitud)+"'"+','+"'"+str(cantidad)+"'"+','+"'"+str(precio)+"'"+','+"'"+str(total)+"'"+','+"'"+str(solicitud_parte[i])+"'"+')"></ion-icon>'+'</td> </tr>'                   
                        # print(solicitud_parte_html)

                        context= {                             
                                'message' : message,
                                'inner': solicitud_parte_html,
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'message' : 'Error en elimina_solicitud_parte',
                                'inner': '',
                        }
                        return JsonResponse(context)

# Elimina abono de la orden de servicio, la entidad sigue exisitiendo pero se desvincula
@login_required(redirect_field_name="")
def elimina_abono(request):
        # Crea la lista de detalle abonos.                      
        if request.method == 'GET':
                try:    
                        servicio = request.GET.get('servicio',"")
                        id_abono = request.GET.get('id_abono',"")
                        if request.user.is_superuser:    
                                message=update_abono_elimina(str(servicio),'abonos',str(id_abono))
                                # Crea mensaje 
                                # qqqqqqq
                                if message == 'El abono fue desvinculado de la orden de servicio':
                                        message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Elimina abono: '+ str(id_abono),str(request.user.username))
                                        if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                                # Anexa el id del mensaje a la orden 
                                                message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                        else:
                               message='No tiene los permisos para realizar esta acción' 
                        # Consulta los abonos ligados a una orden 
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        # Extraemos número de documento de la persona ligada a la orden de servicio
                        identidad=servicio_entidad['identidad']['value']
                        # Calculamos el valor de los abonos de servicio
                        abonos=servicio_entidad['abonos']['value']
                        abonos=abonos.split(',')
                        AbonosInner=''
                        if (len(abonos)>1):
                                for i in range(1,len(abonos)):
                                        abono_entidad=consulta_entidad(str(abonos[i])) # Va por la entidad
                                        abono_entidad['fecha_abono']['value']=abono_entidad['fecha_abono']['value'].split('T')[0]
                                        AbonosInner=AbonosInner+'<tr class="filas_tabla"><td class="th1_abonos">'+str(identidad)+'</td><td class="th2_abonos">'+str(abono_entidad['fecha_abono']['value']).split('T')[0]+'</td><td class="th3_abonos">'+str(abono_entidad['medio_de_pago']['value'])+'</td> <td class="th4_abonos">'+str(abono_entidad['detalle']['value'])+'</td> <td class="th5_abonos">'+str(abono_entidad['valor_abono']['value'])+'</td> <td class="th6_abonos">'+str(abono_entidad['usuario']['value'])+'</td> <td class="th7_abonos"><ion-icon class="list_action" name="trash-outline" onclick="eliminar_abono('+str(abono_entidad)+')"></ion-icon></td></tr>'                                           
                        context= {                             
                                'message' : message,
                                'inner': AbonosInner,
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'message' : 'Error en elimina_abono',
                                'inner': '',
                        }
                        return JsonResponse(context)



# Edita servicio
@login_required(redirect_field_name="")
def actualiza_servicio(request):
        # Crea la lista de detalle abonos.                          
        if request.method == 'GET':
                try:    
                        
                    servicio = request.GET.get('servicio',"")
                    servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad orden de servicio
                    #Evaluamos que el servicio se encuentre en la misma ciudad de quién la quiere observar
                    sede=servicio_entidad['sede']['value']
                    # Extraemos el perfil
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia': 
                        # Recarga los campos que se pueden editar
                        servicio_entidad['lugar']['value'] = request.GET.get('lugar',"")
                        servicio_entidad['tipo_servicio']['value'] = request.GET.get('tipo_servicio',"")
                        servicio_entidad['seguimiento']['value'] = request.GET.get('seguimiento',"")
                        servicio_entidad['nombre']['value'] = request.GET.get('nombre',"")
                        servicio_entidad['identidad']['value'] = request.GET.get('identidad',"")
                        servicio_entidad['direccion']['value'] = request.GET.get('direccion',"")
                        servicio_entidad['localidad']['value'] = request.GET.get('localidad',"")
                        servicio_entidad['telefono']['value'] = request.GET.get('telefono',"")
                        servicio_entidad['email']['value'] = request.GET.get('email',"")
                        servicio_entidad['marca']['value'] = request.GET.get('marca',"")
                        servicio_entidad['producto']['value'] = request.GET.get('producto',"")
                        servicio_entidad['modelo']['value'] = request.GET.get('modelo',"")
                        servicio_entidad['serie']['value'] = request.GET.get('serie',"")
                        servicio_entidad['doc_ref']['value'] = request.GET.get('doc_ref',"")
                        servicio_entidad['falla']['value'] = request.GET.get('falla',"")
                        servicio_entidad['accesorios']['value'] = request.GET.get('accesorios',"")
                        servicio_entidad['observacion']['value'] = request.GET.get('observacion',"")

                        # print(type(servicio_entidad))
                        # Remueve el id y el type del json
                        del servicio_entidad['id']
                        del servicio_entidad['type']
                        # print(servicio_entidad)

                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(servicio)+'/attrs/'
                        headers={"Accept":"application/json"}      
                        response=requests.put(url,headers=headers,json=servicio_entidad)
                        # print(response.status_code)
                        if (response.status_code) == 204:
                                message= "El servicio ha sido actualizado"
                        else :
                                message= "El servicio NO pudo ser actualizado"
                       
                        context= {                             
                                'message' : message,
                                'inner': 'AbonosInner',
                        }
                        return JsonResponse(context)
                    else:
                        context= {
                                'message' : 'La ciudad de sede del usuario no corresponde a la sede de la orden.',
                                'inner': '',
                        }
                        return JsonResponse(context)
                            
                except:
                        context= {
                                'message' : 'Error en actualiza_servicio',
                                'inner': '',
                        }
                        return JsonResponse(context)

@login_required(redirect_field_name="")
def crea_remision(request):
        # Crea una remisión                         
        if request.method == 'GET':
                try:     
                    servicio = request.GET.get('servicio',"")                        
                    forma_pago = request.GET.get('forma_pago',"")
                    medio_pago = request.GET.get('medio_pago',"")
                    fecha_vencimiento = request.GET.get('fecha_vencimiento',"")
                    producto = request.GET.get('producto',0)
                    marca = request.GET.get('marca',0)
                    identificacion = request.GET.get('identificacion',"")
                    cliente = request.GET.get('cliente',"")
                    direccion = request.GET.get('direccion',"")
                    total_abonos = request.GET.get('total_abonos',"")
                    subtotal = request.GET.get('subtotal',"")
                    descuento = request.GET.get('descuento',"")
                    informacion_parte = request.GET.get('informacion_parte',"")
                    total = request.GET.get('total',"")
                    usuario = request.user.username
                        
                    sede=consulta_entidad(str(servicio))['sede']['value']
                    # Extraemos el perfil
                    u=models.UserProfile.objects.get(user__username=str(request.user.username))
                    if u.lugar==sede or u.lugar=='Colombia': 
                        message,id_entidad=crea_entidad_remision(servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte,sede)

                        # Crea mensaje 
                        message_mensaje,id_mensaje=crea_entidad_mensaje(servicio,'Crea remisión: '+ str(id_entidad),str(usuario) )
                        if message_mensaje=='ok': # Retorna ok si el mensaje fue creado                         
                                # Anexa el id del mensaje a la orden 
                                message_mensaje=update_mensaje_servicio(str(servicio),'mensajes',id_mensaje)
                        context= {                             
                                'message' : message,
                                # 'inner': 'solicitud_parte_html',
                        }
                        return JsonResponse(context)
                    else:
                        context= {                             
                                'message' : 'No tiene los permisos para realizar esta acción',
                                # 'inner': 'solicitud_parte_html',
                        }
                        return JsonResponse(context)
                            
                except:
                        context= {
                                'message' : 'Error en crea_solicitud_parte',
                                'inner': '',
                        }
                        return JsonResponse(context)

# Actualiza campo de remisión para evitar parpadeo
@login_required(redirect_field_name="")  
def update_remision(request):
        servicio = request.GET.get('servicio',"")
        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
        
        if (servicio_entidad['remision']['value'] !=''):
                # Existe remisión
                texto_boton_remision='Ver remisión'
                # print(servicio_entidad['remision']['value'])
                entidad_remision=consulta_entidad(servicio_entidad['remision']['value']) # Va por la entidad
                        # print(entidad_remision)
                # print(entidad_remision)
                # Vamos por total remision
                # total_remision='123'
                try:
                        total_remision=entidad_remision['total']['value']
                        funcion_boton_remision='ver_remision_existente()'

                        # Creamos HTML de las partes
                        hmtl_partes=crea_html_remision(entidad_remision['informacion_parte']['value'])
                        context= {
                                # Datos de remisión existente
                                # servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario,informacion_parte):
                                'servicio_ver_remision':servicio,
                                'forma_pago_ver_remision':entidad_remision['forma_pago']['value'],
                                'medio_pago_ver_remision':entidad_remision['medio_pago']['value'],
                                'fecha_vencimiento_ver_remision':entidad_remision['fecha_vencimiento']['value'].split('T')[0],
                                'servicio_ver_remision':entidad_remision['servicio']['value'],
                                'producto_ver_remision':entidad_remision['producto']['value'],
                                'marca_ver_remision':entidad_remision['marca']['value'],
                                'identidad_ver_remision':entidad_remision['identificacion']['value'],
                                'nombre_ver_remision':entidad_remision['cliente']['value'],
                                'direccion_ver_remision':entidad_remision['direccion']['value'],
                                'total_abonos_ver_remision':entidad_remision['total_abonos']['value'],
                                'subtotal_ver_remision':entidad_remision['subtotal']['value'],
                                'descuento_ver_remision':entidad_remision['descuento']['value'],
                                'total_ver_remision':entidad_remision['total']['value'],  
                                'usuario_ver_remision':entidad_remision['usuario']['value'],                                
                                'informacion_parte_ver_remision':entidad_remision['informacion_parte']['value'],         
                                'informacion_parte_ver_remision':hmtl_partes,

                                'hmtl_remision' : hmtl_partes,
                                'texto_boton_remision':texto_boton_remision,
                                'funcion_boton_remision':funcion_boton_remision,
                                'total_remision': str(total_remision),
                        }
                        return JsonResponse(context)
                except:
                        context= {
                        'hmtl_remision' : '',
                        'texto_boton_remision':'Generar remisión',
                        'funcion_boton_remision':'load_remision()',
                        'total_remision':'$ 0',
                        }
                        return JsonResponse(context)

        else:
                context= {
                        'hmtl_remision' : '',
                        'texto_boton_remision':'Generar remisión',
                        'funcion_boton_remision':'load_remision()',
                        'total_remision':'$ 0',
                        }
                return JsonResponse(context)
        

@login_required(redirect_field_name="")  
def imprime_orden_servicio(request):
        # Crea la lista de partes.                          
        if request.method == 'GET':
                try:    
                        # Extraemos datos del servicio
                        servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        no_servicio=str(servicio)
                        # print(servicio_entidad)
                        doc_ref=str(servicio_entidad['doc_ref']['value'])
                        fecha_creacion=servicio_entidad['fecha']['value']
                        fecha_creacion=fecha_creacion.split('.')[0]
                        fecha_creacion=fecha_creacion.split('T')[0]
                        tipo_servicio=servicio_entidad['tipo_servicio']['value']
                        cliente=servicio_entidad['nombre']['value']
                        direccion=servicio_entidad['direccion']['value']
                        localidad=servicio_entidad['localidad']['value']
                        cc_nit=servicio_entidad['identidad']['value']
                        telefono=servicio_entidad['telefono']['value']
                        producto=servicio_entidad['producto']['value']
                        marca=servicio_entidad['marca']['value']
                        modelo=servicio_entidad['modelo']['value']
                        serie=servicio_entidad['serie']['value']
                        sintoma="No fue creado en la entidad"
                        obs=servicio_entidad['observacion']['value']

                        response = HttpResponse(content_type="application/pdf")
                        response["Content-Disposition"] = 'attachment; filename="'+'Orden de servicio '+str(servicio)+'.pdf'+'"'

                        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

                        #Variables diseño
                        w,h=letter
                        margen=50
                        hlogo=55
                        wlogo=100
                        mitadaltura=h/2
                        #Fin Variables diseño

                        #Variables de texto base de datos
                        # no_servicio="254234"
                        # doc_ref="4165234321"
                        # fecha_creacion="06/05/2024"
                        # tipo_servicio="Garantia"
                        # cliente="Miguel Angel Hernandez Bolaños"
                        # direccion="cra 70B #4-36 nueva marsella"
                        # localidad="Kennedy"
                        # cc_nit="1085289791"
                        # telefono="3006875230"
                        # producto="Nevecon"
                        # marca="Samsung"
                        # modelo="RF263BEASL/CO"
                        # serie="0B34H57F32J4HFB"
                        # sintoma="No enfria, no congela"
                        # obs="Retorno de orden 245342"
                        #Fin variables de texto base de datos

                        c = canvas.Canvas(response)

                        c.setFont('Arial', 12)
                        #lineas Guia############################################
                        #c.rect(margen, margen, w-100, h-100, stroke=1, fill=0)
                        #c.line(0, mitadaltura-25, w, mitadaltura-25)
                        #c.line(0, mitadaltura+25, w, mitadaltura+25)
                        #lineas Guia############################################

                        c.setDash(6, 3)
                        c.line(0, mitadaltura, w, mitadaltura)
                        c.setDash()

                        #Creacion de textos fijos orden superior
                        # c.drawImage("static\img\Sertek_Logo.jpg", (margen+5) , (h-margen-hlogo-1), wlogo,hlogo)
                        # c.drawImage("Sertek_Logo.jpg", (margen+5) , (mitadaltura-25-hlogo-2), wlogo,hlogo)

                        data1  = [['SERVICIO TECNICO CALIFICADO SAS'],
                                ['900698640-4'],
                                ['CR 70B#4-36 NUEVA MARSELLA'],
                                ['3003780-3007005978-3007005978'],
                                ['infocliente@sertek.com.co']]
                        data2  = [['No. Servicio:',no_servicio],
                                ['Doc. Ref:', doc_ref],
                                ['Fecha:', fecha_creacion],
                                ['Tipo Servicio:', tipo_servicio]]
                        data3  = [['INFORMACION CLIENTE']]
                        data4  = [['Cliente:', cliente, "CC/Nit:", cc_nit],
                                ['Direccion:', direccion],
                                ['Localidad:', localidad, 'Telefono:', telefono]]
                        data5  =  [["Producto:", producto, "Modelo:", modelo],
                                ["Marca:", marca, "Serie:", serie]]
                        data6  =  [["Sintoma:", sintoma]]
                        data7  =  [["Obs:", obs]]
                        data8  = [["FECHA PRIMERA VISITA:"," YYYY/MM/DD","FECHA REPARACION:", "YYYY/MM/DD","FECHA COMPRA:", "YYYY/MM/DD"]]
                        data9  = [["Diagnostico:"]]
                        data10 = [["Cantidad","Parte/Repuesto","Descripcion","Delivery"],
                                ["","","",""],
                                ["","","",""],
                                ["","","",""]] 
                        data11 = [["","","",""],
                                ["Firma Cliente:","","Tecnico:",""],
                                ["CC. No:","","CC. No:",""],
                                ["","","",""],
                                ["","Fecha Recibido:","YYYY/MM/DD",""]] 

                        tabla1 = Table(data1,colWidths=180,rowHeights=(10))
                        tabla1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                #('BOX', (0,0), (-1,-1), 2, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla1.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla1.drawOn(c, 180, 690)
                        tabla1.drawOn(c, 180, 314)

                        tabla2 = Table(data2,colWidths=80,rowHeights=13)
                        tabla2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                ('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla2.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla2.drawOn(c, w-margen-160, 690)
                        tabla2.drawOn(c, w-margen-160, 314)

                        colWidths = [512]
                        tabla3 = Table(data3,colWidths=colWidths,rowHeights=(13))
                        tabla3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                #('SPAN',(0, 0), (-1, 0))]))

                        tabla3.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla3.drawOn(c, margen, 668)
                        tabla3.drawOn(c, margen, 292)

                        colWidths = [52,300,52,108]
                        tabla4 = Table(data4,colWidths=colWidths,rowHeights=(12))
                        tabla4.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 2), (2, 2), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                #('SPAN',(0, 0), (-1, 0))]))

                        tabla4.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla4.drawOn(c, margen, 632)
                        tabla4.drawOn(c, margen, 256)

                        colWidths = [52,300,52,108]
                        tabla5 = Table(data5,colWidths=colWidths,rowHeights=(12))
                        tabla5.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 1), (2, 1), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                #('SPAN',(0, 0), (-1, 0))]))

                        tabla5.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla5.drawOn(c, margen, 608)
                        tabla5.drawOn(c, margen, 232)

                        colWidths = [50,462]
                        tabla6 = Table(data6,colWidths=colWidths,rowHeights=(12))
                        tabla6.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                #('SPAN',(0, 0), (-1, 0))]))

                        tabla6.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla6.drawOn(c, margen, 596)
                        tabla6.drawOn(c, margen, 220)

                        colWidths = [50,462]
                        tabla7 = Table(data7,colWidths=colWidths,rowHeights=(12))
                        tabla7.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                #('SPAN',(0, 0), (-1, 0))]))

                        tabla7.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla7.drawOn(c, margen, 584)
                        tabla7.drawOn(c, margen, 208)

                        colWidths = [110,71,100,71,90,70]
                        tabla8 = Table(data8,colWidths=colWidths,rowHeights=(12))
                        tabla8.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 8),
                                                ('TEXTCOLOR', (1, 0), (1, 0), colors.gray),
                                                ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
                                                ('TEXTCOLOR', (3, 0), (3, 0), colors.gray),
                                                ('FONTNAME', (3, 0), (3, 0), 'Helvetica-Bold'),
                                                ('TEXTCOLOR', (5, 0), (5, 0), colors.gray),
                                                ('FONTNAME', (5, 0), (5, 0), 'Helvetica-Bold'),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla8.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla8.drawOn(c, margen, 572)
                        tabla8.drawOn(c, margen, 196)

                        colWidths = [512]
                        tabla9 = Table(data9,colWidths=colWidths,rowHeights=(50))
                        tabla9.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'TOP')]))

                        tabla9.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla9.drawOn(c, margen, 522)
                        tabla9.drawOn(c, margen, 146)

                        colWidths = [50,100,250,112]
                        tabla10 = Table(data10,colWidths=colWidths,rowHeights=(13))
                        tabla10.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                ('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla10.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla10.drawOn(c, margen, 470)
                        tabla10.drawOn(c, margen, 94)

                        colWidths = [60,196,60,196]
                        rowHeights= [8,13,13,8,13]
                        tabla11 = Table(data11,colWidths=colWidths,rowHeights=rowHeights)
                        tabla11.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('ALIGN', (1, 4), (1, 4), 'RIGHT'),
                                                ('TEXTCOLOR', (2, 4), (2, 4), colors.gray),
                                                ('FONTNAME', (2, 4), (2, 4), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 1), (2, 1), 'Helvetica-Bold'),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                                #('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black)
                                                ]))

                        tabla11.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla11.drawOn(c, margen, 416)
                        tabla11.drawOn(c, margen, 40)

                        c.save()
                        context= {                             
                                'message' : 'message',
                                'inner': 'solicitud_parte_html',
                        }
                        
                        return response
                except:
                        context= {
                                'message' : 'Error enviando coumento',
                                'inner': '',
                        }
                        return JsonResponse(context)
@login_required(redirect_field_name="")             
def imprime_remision(request):
        # Crea la lista de partes.                          
        if request.method == 'GET':
                try:    
                        # Extraemos datos del servicio
                        servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        #  Vamos por la remisión
                        remision_entidad=consulta_entidad(str(servicio_entidad['remision']['value'])) # Va por la entidad


                        # no_servicio=str(servicio)
                        # # print(servicio_entidad)
                        # doc_ref=str(servicio_entidad['doc_ref']['value'])
                        # fecha_creacion=servicio_entidad['fecha']['value']
                        # fecha_creacion=fecha_creacion.split('.')[0]
                        # fecha_creacion=fecha_creacion.split('T')[0]
                        # tipo_servicio=servicio_entidad['tipo_servicio']['value']
                        # cliente=servicio_entidad['nombre']['value']
                        # direccion=servicio_entidad['direccion']['value']
                        # localidad=servicio_entidad['localidad']['value']
                        # cc_nit=servicio_entidad['identidad']['value']
                        # telefono=servicio_entidad['telefono']['value']
                        # producto=servicio_entidad['producto']['value']
                        # marca=servicio_entidad['marca']['value']
                        # modelo=servicio_entidad['modelo']['value']
                        # serie=servicio_entidad['serie']['value']
                        # sintoma="No fue creado en la entidad"
                        # obs=servicio_entidad['observacion']['value']

                        response = HttpResponse(content_type="application/pdf")
                        response["Content-Disposition"] = 'attachment; filename="'+'Remisión_'+str(servicio)+'.pdf'+'"'
                        # response["Content-Disposition"] = 'attachment; filename="'+'Orden de servicio '+str('test')+'.pdf'+'"'

                        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

                        #Variables diseño
                        w,h=letter
                        margen=50
                        hlogo=55
                        wlogo=100
                        mitadaltura=h/2
                        #Fin Variables diseño

                        #Variables de texto base de datos
                        no_servicio=remision_entidad['servicio']['value']
                        no_remision_split=remision_entidad['id'].split('_')
                        num_remision=no_remision_split[1]+'_'+no_remision_split[2]
                        no_remision=num_remision
                        try:
                                fecha_remision=remision_entidad['fecha_creacion']['value'].split('T')[0]
                        except:
                                fecha_remision='No data'
                        # doc_ref="4165234321"
                        # fecha_creacion=remision_entidad['fecha_creacion']['value']
                        # tipo_servicio="Garantia"
                        cliente=remision_entidad['cliente']['value']
                        direccion=remision_entidad['direccion']['value']
                        localidad=servicio_entidad['localidad']['value']
                        cc_nit=remision_entidad['identificacion']['value']
                        telefono=servicio_entidad['telefono']['value']
                        # producto="Nevecon"
                        # marca="Samsung"
                        # modelo="RF263BEASL/CO"
                        # serie="0B34H57F32J4HFB"
                        # sintoma="No enfria, no congela"
                        # obs="Retorno de orden 245342"
                        #Fin variables de texto base de datos

                        c = canvas.Canvas(response)

                        c.setFont('Arial', 12)
                        #lineas Guia############################################
                        #c.rect(margen, margen, w-100, h-100, stroke=1, fill=0)
                        #c.line(0, mitadaltura-25, w, mitadaltura-25)
                        #c.line(0, mitadaltura+25, w, mitadaltura+25)
                        #lineas Guia############################################

                        #Creacion de textos fijos orden superior
                        # c.drawImage('../img/Sertek_Logo.jpg', (margen+5) , (h-margen-hlogo-1), wlogo,hlogo)
                        # logo = ImageReader('/static/img/Sertek_Logo.jpg')  
                        # settings.BASE_DIR+'/blog/static/img/logo.png'
                        # print(str(settings.STATIC_URL))
                        # print(str(settings.BASE_DIR)+'\crear_servicio\static\img\Sertek_Logo.png')
                        # logo = ImageReader(str(settings.BASE_DIR)+'/crear_servicio/static/img/Sertek_Logo.png') 
                        # print(settings.BASE_DIR+'/crear_servicio/static/img/Sertek_Logo.png')
                        # logo = ImageReader(settings.BASE_DIR+'/crear_servicio/static/img/Sertek_Logo.png') 
                        # c.drawImage(str(settings.BASE_DIR)+'\crear_servicio\static\img\Sertek_Logo.png', (margen+5) , (h-margen-hlogo-1), wlogo,hlogo)

                        data1  = [['SERVICIO TECNICO CALIFICADO SAS'],
                                ['900698640-4'],
                                ['CR 70B#4-36 NUEVA MARSELLA'],
                                ['3003780-3007005978-3007005978'],
                                ['infocliente@sertek.com.co']]
                        data3  = [['INFORMACION CLIENTE']]
                        data4  = [['Cliente:', cliente, "CC/Nit:", cc_nit],
                                ['Direccion:', direccion],
                                ['Localidad:', localidad, 'Telefono:', telefono],
                                ['No. Orden:', no_servicio]]

                        data5  = [['DETALLE','PRECIO','CANTIDAD','DESC','TOTAL']]


                        tabla1 = Table(data1,colWidths=180,rowHeights=(10))
                        tabla1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                #('BOX', (0,0), (-1,-1), 2, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla1.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla1.drawOn(c, 180, 690)

                        def add_bold_text(c):
                                c.setFont("Helvetica-Bold", 14)  
                                c.drawString(390, 710, "REMISION No.: ")
                                c.drawString(500, 710, no_remision)

                        def add_small_text(c):
                                c.setFont('Arial', 10)
                                c.drawString(390, 690, "Fecha: ")
                                c.drawString(430, 690, fecha_remision)

                        add_bold_text(c)
                        add_small_text(c)

                        colWidths = [512]
                        tabla3 = Table(data3,colWidths=colWidths,rowHeights=(16))
                        tabla3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                #('SPAN',(0, 0), (-1, 0)),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

                        tabla3.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla3.drawOn(c, margen, 658)

                        colWidths = [58,300,52,102]
                        tabla4 = Table(data4,colWidths=colWidths,rowHeights=(16))
                        tabla4.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
                                                ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
                                                ('FONTNAME', (2, 2), (2, 2), 'Helvetica-Bold'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                #('SPAN',(0, 0), (-1, 0)),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                

                        tabla4.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla4.drawOn(c, margen, 594)

                        colWidths = [264,62,62,62,62]
                        tabla5 = Table(data5,colWidths=colWidths,rowHeights=(16))
                        tabla5.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                                                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                                ('ALIGN', (0,0), (0,0), 'LEFT'),
                                                ('FONTSIZE', (0,0), (-1,-1), 10),
                                                ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),  # Borde inferior
                                                #('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                #('GRID', (0,0), (-1,-1), 1, colors.black),
                                                #('SPAN',(0, 0), (-1, 0)),
                                                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
                                                

                        tabla5.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                        tabla5.drawOn(c, margen, 570)

                        partes_string=remision_entidad['informacion_parte']['value']
                        partes_string=partes_string.split('divisor_item')
                        # print(partes_string)
                        for i in range(0,len(partes_string)-1):
                                # print(partes_string[i])
                                partes_string_aux=partes_string[i].split(',')
                                # print(partes_string_aux)
                                # html_partes=html_partes+"""
                                # Nombre 0, referencia 1, fecha de solcitud 2, cantidad 3, precio de venta 4, total 5, descuento 6
                                data6  = [[partes_string_aux[1]+';'+partes_string_aux[0], partes_string_aux[4] , partes_string_aux[3] , partes_string_aux[6] , partes_string_aux[5]]]
                                tabla6 = Table(data6,colWidths=colWidths,rowHeights=(16))
                                tabla6.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                                                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                                        ('ALIGN', (0,0), (0,0), 'LEFT'),
                                                        ('FONTSIZE', (0,0), (-1,-1), 10),
                                                        # ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),  # Borde inferior
                                                        #('BOX', (0,0), (-1,-1), 1, colors.black),  # Agrega un borde exterior
                                                        ('GRID', (0,0), (-1,-1), 1, colors.black),
                                                        #('SPAN',(0, 0), (-1, 0)),
                                                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))                                                

                                tabla6.wrapOn(c, pagesizes.letter[0], pagesizes.letter[1])
                                tabla6.drawOn(c, margen, 540-(i*16))


                        c.save()
                        context= {                             
                                'message' : 'message',
                                'inner': 'solicitud_parte_html',
                        }
                        
                        return response
                except:
                        context= {
                                'message' : 'Error enviando coumento',
                                'inner': '',
                        }
                        return JsonResponse(context)