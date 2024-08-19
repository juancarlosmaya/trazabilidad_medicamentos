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

from django.contrib.auth.decorators import user_passes_test


from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]

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




def crea_entidad_item(referencia,nombre_parte,cantidad,precio,observacion,fecha_actualizacion,ciudad,delivery,marca):
        try:
                ContextDataJSON={"id": "",
                                "type": "parte",

                                "referencia": {
                                "value": "",
                                "type": "String"
                                },
                                "cantidad": {
                                "value": 0,
                                "type": "integer"
                                },
                                "descripcion": {
                                "value": '',
                                "type": "String"
                                },
                                "nombre_parte": {
                                "value": "",
                                "type": "String"
                                },
                                "precio":{
                                "value": "",
                                "type": "String"
                                },
                                "observacion":{
                                "value": "",
                                "type": "String"
                                },
                                "ciudad":{
                                "value": "",
                                "type": "String"
                                },
                                "fecha_actualizacion":{
                                "value": "",
                                "type": "DateTime"
                                },
                                "delivery":{
                                "value": "",
                                "type": "String"
                                },
                                "marca":{
                                "value": "",
                                "type": "String"
                                },
                                "activo":{
                                "value": 1,
                                "type": "integer"
                                },
                                "tipo":{
                                "value": "parte",
                                "type": "String"
                                }
                                }
                
                ContextDataJSON['type']='parte' 

                ContextDataJSON['referencia']['value']=referencia     
                ContextDataJSON['cantidad']['value']=cantidad
                ContextDataJSON['nombre_parte']['value']=nombre_parte
                ContextDataJSON['precio']['value']=int(precio)
                ContextDataJSON['observacion']['value']=observacion
                ContextDataJSON['fecha_actualizacion']['value']=fecha_actualizacion
                ContextDataJSON['ciudad']['value']=ciudad
                ContextDataJSON['delivery']['value']=delivery
                ContextDataJSON['marca']['value']=marca
                
                ContextDataJSON['tipo']['value']='parte' # Para filtrar datos desde fiware orion
                crea_parte=0
                while(crea_parte==0):
                        ContextDataJSON['id']='parte_'+str(random.randint(0,1000000))  # Nombre de la entidad abono abono_servicio_+randit()
                        # ContextDataJSON['id']='abono_'+str(servicio)  # Nombre de la entidad abono abono_servicio_+randit()
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
                        headers={"Accept":"application/json"}
                        response= requests.post(url,headers=headers,json=ContextDataJSON) 
                        # print(response.status_code)
                        if (response.status_code) == 201:
                                crea_parte=1
                                break
                        else:
                               time.sleep(1)
                return "El item fue creado. id=" , ContextDataJSON['id']

        except:
                return "La parte NO pudo ser creada",''

def edita_entidad_item(id_item,referencia,nombre_parte,cantidad,precio,observacion,fecha_actualizacion,ciudad,delivery,marca):
        try:
                servicio_entidad=consulta_entidad(str(id_item)) # Va por la entidad item

                servicio_entidad['referencia']['value']=referencia     
                servicio_entidad['cantidad']['value']=cantidad
                servicio_entidad['nombre_parte']['value']=nombre_parte
                servicio_entidad['precio']['value']=int(precio)
                servicio_entidad['observacion']['value']=observacion
                servicio_entidad['fecha_actualizacion']['value']=fecha_actualizacion
                servicio_entidad['ciudad']['value']=ciudad
                servicio_entidad['delivery']['value']=delivery
                servicio_entidad['marca']['value']=marca

                # print(type(servicio_entidad))
                # Remueve el id y el type del json
                del servicio_entidad['id']
                del servicio_entidad['type']
                # print(servicio_entidad)
                
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(id_item)+'/attrs/'
                headers={"Accept":"application/json"}      
                response=requests.put(url,headers=headers,json=servicio_entidad)
                # print(response.status_code)
                if (response.status_code) == 204:
                        message= "El item ha sido actualizado"
                else :
                        message= "El item NO pudo ser actualizado"

                return message

        except:
                return "El item NO pudo ser creada"





# Consulta todos los items
def consulta_items(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3,atributo_4,valor_4):
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
#     if (valor_3==''):
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
def crear_item(request):                         
        if request.method == 'GET':
                try:   
                        # referencia,nombre_parte,cantidad,precio,observacion,fecha_actualizacion,ciudad,delivery,marca 
                        referencia = request.GET.get('referencia',"").upper()
                        nombre_parte = request.GET.get('nombre_parte',"").upper()
                        cantidad = request.GET.get('cantidad',"")
                        precio = request.GET.get('precio',"")                                 
                        observacion = request.GET.get('observacion',"")
                        ciudad = request.GET.get('ciudad',"") 
                        marca = request.GET.get('marca',"").upper()  
                        fecha_actualizacion=str(datetime.date.today())
                        delivery=''
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        if u.lugar!='Colombia':
                                ciudad=u.lugar
                                message=crea_entidad_item(referencia, nombre_parte, cantidad, precio, observacion, fecha_actualizacion, ciudad, delivery, marca)
                        else:
                               ciudad = request.GET.get('ciudad',"")
                               message=crea_entidad_item(referencia, nombre_parte, cantidad, precio, observacion, fecha_actualizacion, ciudad, delivery, marca)

                        # message=crea_entidad_item(referencia, nombre_parte, cantidad, precio, observacion, fecha_actualizacion, ciudad, delivery, marca)
                        return JsonResponse(message,  safe=False)
                except:
                        return JsonResponse(None,  safe=False)

@login_required(redirect_field_name="")
def editar_item(request):                         
        if request.method == 'GET':
                if request.user.is_superuser: 

                        try:   
                                # referencia,nombre_parte,cantidad,precio,observacion,fecha_actualizacion,ciudad,delivery,marca 
                                id_item = request.GET.get('id_item',"")
                                referencia = request.GET.get('referencia',"").upper()
                                nombre_parte = request.GET.get('nombre_parte',"").upper()
                                cantidad = request.GET.get('cantidad',"")
                                precio = request.GET.get('precio',"")                                 
                                observacion = request.GET.get('observacion',"")
                                ciudad = request.GET.get('ciudad',"") 
                                marca = request.GET.get('marca',"").upper()   
                                fecha_actualizacion=str(datetime.date.today())
                                delivery=''
                                # Extraemos el perfil
                                u=models.UserProfile.objects.get(user__username=str(request.user.username))
                                if u.lugar==ciudad or u.lugar=='Colombia':
                                        message=edita_entidad_item(id_item,referencia, nombre_parte, cantidad, precio, observacion, fecha_actualizacion, ciudad, delivery, marca)
                                        context= {                             
                                                'message' : message,
                                        }
                                        return JsonResponse(context)
                                else:
                                        context= {                             
                                                'message' : 'El lugar de usuario no corresponde con la sede del item.',
                                        }
                                        return JsonResponse(context)
                        except:
                                return JsonResponse(None,  safe=False)
                else:
                        message="No tiene los permisos para realizar esta acción"
                        context={
                        'message':message,
                        }
                        return JsonResponse(context,  safe=False)
                       
                
@login_required(redirect_field_name="")
def buscar_items_filtro(request):
        # Busca todos los items                                                    
        if request.method == 'GET':
                try:    
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")

                        activo = request.GET.get('activo',"1")  
                        atributo = request.GET.get('atributo',"")
                        search = request.GET.get('search',"")
                        # search=urllib.parse.unquote(search.upper())
                        search=urllib.parse.unquote(search.upper())

                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))

                        total_enity,dict_entity=consulta_items(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo','parte',atributo,search,'activo',activo,'ciudad',u.lugar)
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_items(int(por_pagina),0,'tipo','parte',atributo,search,'activo',activo,'ciudad',u.lugar)
                                actual_page=1

                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        innerHtml=""
                        for i in range(0,len(dict_entity)):
                                innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1_servicios">'+str(dict_entity[i]['marca']['value'])+'</td>'  + '<td class="th2_servicios">'+str(dict_entity[i]['referencia']['value'])+'</td>' + '<td class="th3_servicios">'+urllib.parse.unquote(str(dict_entity[i]['nombre_parte']['value']))+'</td>' + '<td class="th4_servicios">'+str(dict_entity[i]['precio']['value'])+'</td>' + '<td class="th5_servicios">'+str(dict_entity[i]['cantidad']['value'])+'</td>' + '<td class="th6_servicios">'+str(dict_entity[i]['observacion']['value'])+'</td>' + '<td class="th7_servicios"> <ion-icon class="select_cliente" name="pencil-outline" onclick="editar_item('+str(dict_entity[i])+')"></ion-icon> <ion-icon class="select_cliente" name="trash-outline" onclick="eliminar_item('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'                  
                                
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
def inventario(request):
        try:    
                # Extraemos el perfil
                u=models.UserProfile.objects.get(user__username=str(request.user.username))
                if u.cambio_ciudad==True:
                        lista=models.UserProfile.lugar_lista # Va por la lista de ciudad del MOdels usuarios
                        innerHtml='<option value="" disabled selected hidden>Sede</option>'                        
                        for i in range(0,len(lista)-1):                                 
                                        innerHtml=innerHtml+ '<option  value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'                                                      
                        context= {
                                'lista_ciudades':innerHtml ,
                                }
                        return render(request, 'pages/inventario.html', context) 
                else:  
                        context= {
                                'lista_ciudades':'<option  value="'+str(u.lugar)+'">'+str(u.lugar)+'</option>'  ,
                                }
                        return render(request, 'pages/inventario.html', context) 
        except:
                context={
                        }
                return render(request, 'pages/inventario.html', context)


@login_required(redirect_field_name="")
def elimina_item(request):  # Elimina item, sigue exsitiendo como entidad
        try:    
                item_id = request.GET.get('item_id',"") 
                if request.user.is_superuser: 
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        if u.lugar!='Colombia':
                                # Verifica que la ciudad corresponda al item qye se desea borrar vvvvv
                                ciudad_item=consulta_entidad(str(item_id))['ciudad']['value']
                                if ciudad_item==u.lugar:
                                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+item_id+'/attrs/'+'activo'+'/value'
                                        headers={"Content-Type":"text/plain"}        
                                        response=requests.put(url,headers=headers,json=0)
                                        if (response.status_code) == 204:
                                                message_1="El item fue eliminado"
                                                context={
                                                'message':message_1,
                                                }
                                                return JsonResponse(context,  safe=False)
                                        else :
                                                message_1="El item NO fue eliminado"
                                                context={
                                                'message':message_1,
                                                }
                                                return JsonResponse(context,  safe=False)
                                else:
                                        message_1="La sede del usuario no corresponde a la sede en donde se encuentra el item."
                                        context={
                                        'message':message_1,
                                        }
                                        return JsonResponse(context,  safe=False)
                        else:
                                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+item_id+'/attrs/'+'activo'+'/value'
                                headers={"Content-Type":"text/plain"}        
                                response=requests.put(url,headers=headers,json=0)
                                if (response.status_code) == 204:
                                        message_1="El item fue eliminado"
                                        context={
                                        'message':message_1,
                                        }
                                        return JsonResponse(context,  safe=False)
                                else :
                                        message_1="El item NO fue eliminado"
                                        context={
                                        'message':message_1,
                                        }
                                        return JsonResponse(context,  safe=False)
                else:
                        message_1="No tiene los permisos para realizar esta acción"
                        context={
                        'message':message_1,
                        }
                        return JsonResponse(context,  safe=False)
                             
        except:
                context={
                        'message':"El item NO fue eliminado",
                        }
                return JsonResponse(context,  safe=False)