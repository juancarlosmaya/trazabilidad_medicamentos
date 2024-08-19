from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import requests
import json
import math
from django.http import JsonResponse
import urllib.parse
import datetime 
from django.contrib.auth.decorators import login_required

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

# Realiza y registra pago
@login_required(redirect_field_name="")
def realiza_pago(request):  # Acá voy
        try:
# Cargamos las solicitudes de parte ligadas a la orden
                # servicio = request.GET.get('servicio',"")
                # servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                if request.user.is_superuser:  
                        parte_id = request.GET.get('parte_id',"")
                        parte_entidad=consulta_entidad(str(parte_id)) # Va por la entidad

                        servicio=parte_entidad['servicio']['value']
                        # servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        

                        id_estado = request.GET.get('id_estado',"")
                        
                        estado=consulta_entidad(str(id_estado)) # Va por la entidad estado

                        if estado['pagado']['value']==1:
                                context={
                                'message':'No fue posible realizar el pago, se registró un pago anterior.',
                                }
                                return JsonResponse(context,  safe=False)
                        # estado_entidad=consulta_entidad(str(id_estado)) # Va por la entidad
                        # print(id_estado)


                        # Extraemos el nombre de la remisión para saber si ya se realizó el pago
                        # y en qué manera se realizó el pago . Contado o transferencia
                        # para que de esta manera construir la ecuación de pago.
                        medio_pago_aux='efectivo'
                        try:
                                remision=servicio_entidad['remision']['value']
                                remision_entidad=consulta_entidad(str(remision)) # Va por la entidad de remisión
                                medio_pago=remision_entidad['medio_pago']['value'] # Extraemos medio pago
                                if (medio_pago!='efectivo'):
                                        medio_pago_aux='otro'
                        except:
                                # En caso de que no exista la remisión se debe crear antes de realizar el pago 
                                context={
                                'message':'No Existe remisión, no fue posible realizar el pago',
                                }
                                return JsonResponse(context,  safe=False)
                        
                        # Verificamos métodos de pago, si hay al menos una transacción electrónica consideramos todo el pago como electrónico
                        try:
                                abonos=servicio_entidad['abonos']['value']
                                abonos=abonos.split(',')
                                # print(abonos)-----------
                                for i in range(1,len(abonos)):                          
                                        entidad_abono=consulta_entidad(abonos[i])
                                        print(entidad_abono['medio_de_pago']['value'])
                                        if (entidad_abono['medio_de_pago']['value']!='efectivo' ):
                                                medio_pago_aux='otro'
                        except:
                        #        print('No hay abonos')
                                pass              

                        if  medio_pago_aux=='efectivo':
                                valor=float(parte_entidad['precio']['value'])/2
                        else:
                                precio=float(parte_entidad['precio']['value'])
                                valor=(precio - ( precio*float(consulta_entidad('IVA')['valor']['value']))/100)/2

                        # Registra el pago en la entidad estado pagado int  valor_pagado  fecha_pago
                        # Actualiza campo estado
                        ContextDataJSON={"pagado": {
                                        "value": 1,
                                        "type": "integer"
                                        },
                                        "fecha_pago": {
                                        "value": str(datetime.date.today()) ,
                                        "type": "DateTime"
                                        },
                                        "valor_pagado": {
                                        "value": int(valor) ,
                                        "type": "integer"
                                        }
                                        }
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(id_estado)+'/attrs/'
                        headers={"Accept":"application/json"}       
                        # response=requests.put(url,headers=headers,json=str(value))
                        response=requests.post(url,headers=headers,json=ContextDataJSON)
                        print(response.text)
                        if (response.status_code) == 204:
                                context={
                                'message':'El pago realizado es de '+str(valor),
                                }
                                return JsonResponse(context,  safe=False)
                        else :
                                context={
                                'message':'El pago NO fue registrado'
                                }
                                return JsonResponse(context,  safe=False)
                else:
                        context={
                        'message':'No cuenta con los permisos necesarios'
                        }
                        return JsonResponse(context,  safe=False)

        except:
                context={
                       'message':'El pago NO fue registrado, intente nuevamente',
                        }
                return JsonResponse(context,  safe=False)

# Carga valor seleccionado
@login_required(redirect_field_name="")
def carga_valor(request):
        try:    
                if request.user.is_superuser:  
                        # Cargamos las solicitudes de parte ligadas a la orden
                        servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad

                        parte_id = request.GET.get('parte_id',"")
                        parte_entidad=consulta_entidad(str(parte_id)) # Va por la entidad




                        # Extraemos el nombre de la remisión para saber si ya se realizó el pago
                        # y en qué manera se realizó el pago . Contado o transferencia
                        # para que de esta manera construir la ecuación de pago.
                        medio_pago_aux='efectivo'
                        try:
                                remision=servicio_entidad['remision']['value']
                                remision_entidad=consulta_entidad(str(remision)) # Va por la entidad de remisión
                                medio_pago=remision_entidad['medio_pago']['value'] # Extraemos medio pago
                                if (medio_pago!='efectivo'):
                                        medio_pago_aux='otro'
                        except:
                                # En caso de que no exista la remisión se debe crear antes de realizar el pago 
                                context={
                                'partes':'<tr><th colspan="4" style="color: red;" >No Existe remisión</th></tr>',
                                'forma_pago':'',
                                }
                                return JsonResponse(context,  safe=False)
                        
                        # Verificamos métodos de pago, si hay al menos una transacción electrónica consideramos todo el pago como electrónico
                        try:
                                abonos=servicio_entidad['abonos']['value']
                                abonos=abonos.split(',')
                                # print(abonos)
                                for i in range(1,len(abonos)):                          
                                        entidad_abono=consulta_entidad(abonos[i])
                                        print(entidad_abono['medio_de_pago']['value'])
                                        if (entidad_abono['medio_de_pago']['value']!='efectivo' ):
                                                medio_pago_aux='otro'
                        except:
                        #        print('No hay abonos')
                                pass              

                        if  medio_pago_aux=='efectivo':
                                valor=float(parte_entidad['precio']['value'])/2
                        else:
                                precio=float(parte_entidad['precio']['value'])
                                valor=(precio - ( precio*float(consulta_entidad('IVA')['valor']['value']))/100)/2
                        context={
                                'valor':valor,
                                # 'forma_pago':forma_pago,
                                }
                        return JsonResponse(context,  safe=False)
                else:   
                        context={
                                'valor':'',
                                # 'forma_pago':forma_pago,
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                       'valor':'',
                #        'forma_pago':'',
                        }
                return JsonResponse(context,  safe=False)

# Carga las partes para pagos
@login_required(redirect_field_name="")
def get_partes(request):
        try:
                if request.user.is_superuser:  
                        # Cargamos las solicitudes de parte ligadas a la orden
                        servicio = request.GET.get('servicio',"")
                        servicio_entidad=consulta_entidad(str(servicio)) # Va por la entidad
                        remision=servicio_entidad['remision']['value']
                        if remision!='':

                        # Verificamos que existan remisiones activas y ligadas a l orden de servicio

                        # # Extraemos el nombre de la remisión para saber si ya se realizó el pago
                        # # y en qué manera se realizó el pago . Contado o transferencia
                        # # para que de esta manera construir la ecuación de pago.
                        # try:
                        #         remision=servicio_entidad['remision']['value']
                        #         remision_entidad=consulta_entidad(str(remision)) # Va por la entidad de remisión
                        #         medio_pago=remision_entidad['medio_pago']['value'] # Extraemos medio pago
                        #         print(medio_pago)
                        # except:
                        #         # En caso de que no exista la remisión se debe crear antes de realizar el pago 
                        #         context={
                        #         'partes':'<tr><th colspan="4" style="color: red;" >No Existe remisión</th></tr>',
                        #         'forma_pago':'',
                        #         }
                        #         return JsonResponse(context,  safe=False)
                        
                        # # Verificamos métodos de pago, si hay al menos una transacción electrónica consideramos todo el pago como electrónico
                        # try:
                        #         abonos=servicio_entidad['abonos']['value']
                        #         abonos=abonos.split(',')
                        #         print(abonos)
                        #         total_abonos=0
                        #         forma_pago=''
                        #         for i in range(1,len(abonos)):                          
                        #                 entidad_abono=consulta_entidad(abonos[i])
                        #                 print(entidad_abono['medio_de_pago']['value'])
                        #                 # if (entidad_abono['medio_de_pago']['value']== ):
                        # except:
                        #        print('No hay abonos')
                        #        pass

                        


                                solicitud_parte=servicio_entidad['solicitud_parte']['value']
                                solicitud_parte=solicitud_parte.split(',')
                                solicitud_parte_html=''
                                for i in range(1,len(solicitud_parte)): 
                                        solicitud_parte_entidad=consulta_entidad(solicitud_parte[i])  
                                        nombre_parte=str(solicitud_parte_entidad['nombre_parte']['value'])  
                                        referencia=str(solicitud_parte_entidad['referencia']['value'])
                                        cantidad=str(solicitud_parte_entidad['cantidad']['value'])
                                        precio=str(solicitud_parte_entidad['precio']['value'])
                                        total=int(precio)*int(cantidad)
                                        fecha_solicitud=str(solicitud_parte_entidad['fecha_solicitud']['value']) 
                                        fecha_solicitud=fecha_solicitud.split('.')[0]
                                        fecha_solicitud=fecha_solicitud.split('T')[0]
                                        solicitud_parte_html=solicitud_parte_html+'<tr class="filas_tabla"><td class="th1">'+str(nombre_parte)+'</td><td class="th2">'+str(fecha_solicitud)+'</td> <td class="th3">'+str(precio)+'</td>  <td class="th4">'+ '<ion-icon class="select_cliente" name="checkmark-done-outline" onclick="seleccion_pago('+str(solicitud_parte_entidad)+')"></ion-icon>'+'</td> </tr>'                   

                                context={
                                        'partes':solicitud_parte_html,
                                        # 'forma_pago':forma_pago,
                                        }
                                return JsonResponse(context,  safe=False)
                        else:
                                #En caso de que no exista la remisión se debe crear antes de realizar el pago 
                                context={
                                'partes':'<tr><th colspan="4" style="color: red;" >No Existe remisión</th></tr>',
                                'forma_pago':'',
                                }
                                return JsonResponse(context,  safe=False)
                else:
                        context={
                                'partes':'No cuenta con los permisos necesarios.',
                                }
                        return JsonResponse(context,  safe=False)
        except:
                context={
                       'partes':'',
                        }
                return JsonResponse(context,  safe=False)
# Realiza consulta
def query_orion(paginado,offset,attr):
    attr_aux=''       
    for i in range(0,len(attr)):
        if (attr[i][1]!=''):
                if (attr[i][0]=='fecha_inicio'):
                        attr_aux=attr_aux+str('fecha_estado')+'>='+str(attr[i][1])+';'
                if (attr[i][0]=='fecha_fin'):
                        attr_aux=attr_aux+str('fecha_estado')+'<='+str(attr[i][1])+';'
                if (attr[i][0]!='fecha_inicio' and attr[i][0]!='fecha_fin' ):
                       attr_aux=attr_aux+str(attr[i][0])+'=='+str(attr[i][1])+';'              
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+attr_aux+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
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
def search(request):
        if request.user.is_superuser:                                                     
                if request.method == 'GET':
                        try:    
                                por_pagina = request.GET.get('por_pagina',"1")
                                actual_page = request.GET.get('actual_page',"1")
                                fecha_inicio = request.GET.get('fecha_inicio',"")
                                fecha_fin = request.GET.get('fecha_fin',"")
                                activa = request.GET.get('activa',"")
                                estado = request.GET.get('estado',"")
                                tecnico = urllib.parse.unquote(request.GET.get('tecnico',""))
                                # print(tecnico)
                                if tecnico=='Todos':
                                        tecnico=''
                                attr=[['tipo','estado'],['tecnico',tecnico],['pagado',estado],['fecha_inicio',fecha_inicio],['fecha_fin',fecha_fin],['activa',activa]]                        
                                total_enity,dict_entity=query_orion(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),attr)
                                if (len(dict_entity)==0) and (actual_page!='1'):
                                        total_enity,dict_entity=query_orion(int(por_pagina),0,attr)
                                        actual_page=1                        
                                num_pages=math.ceil(int(total_enity)/int(por_pagina))
                                innerHtml=""
                                for i in range(0,len(dict_entity)):
                                        estado_pago='Indeterminado'  
                                        try:
                                                if (dict_entity[i]['pagado']['value']==0):
                                                        estado_pago='Sin pagar'
                                                if (dict_entity[i]['pagado']['value']==1):
                                                        estado_pago='Pagado'
                                        except:
                                                estado_pago='Indeterminado'   
                                        innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1_servicios">'+str(dict_entity[i]['servicio']['value'])+'</td>'  + '<td class="th2_servicios">'+str(dict_entity[i]['tecnico']['value'])+'</td>' + '<td class="th3_servicios">'+str(dict_entity[i]['estado']['value'])+'</td>' + '<td class="th4_servicios">'+str(dict_entity[i]['fecha_estado']['value'].split('T')[0] )+'</td>' + '<td class="th5_servicios">'+str(dict_entity[i]['usuario']['value'])+'</td>' + '<td class="th6_servicios">'+str(estado_pago)+'</td>' + '<td class="th7_servicios"> <ion-icon class="select_cliente" name="cash-outline" onclick="pagar('+str(dict_entity[i])+')"></ion-icon> <ion-icon class="select_cliente" name="eye-outline" onclick="ver_servicio('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'                                                 
                                        # Agregar dos líneas vacías para cuestión de visualización
                                for i in range(0,1):
                                        # innerHtml=innerHtml+ '<tr class="filas_vacia">' + '<td class="th1_servicios">'+''+'</td>'  + '<td class="th2_servicios">'+''+'</td>' + '<td class="th3_servicios">'+''+'</td>' + '<td class="th4_servicios">'+''+'</td>' + '<td class="th5_servicios">'+''+'</td>' + '<td class="th6_servicios">'+''+'</td>' + '<td class="th7_servicios"> </td>' +'</tr>'                                                 
                                        innerHtml=innerHtml+'<div style="height: 60px;" ></div>'
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
        else:
                context= {
                        'inner':'No cuenta con los permisos necesarios',
                        'actual_page' : '0',
                        'num_pages' : '0',
                }
                return JsonResponse(context,  safe=False)
                

def lista_tecnicos():                                                
                try:    
                        User = get_user_model()
                        users = User.objects.all()
                        innerHtml=""
                        for i in range(0,len(users)):
                                u=User.objects.get(username=str(users[i]))
                                if (u.userprofile.rol=='3') and (u.userprofile.realiza_servicio== True):  # 3 es técnico                                       
                                        innerHtml=innerHtml+ '<option value="'+str(users[i].username)+'">'+str(users[i].get_full_name())+'</option>'                                                      
                        context= {
                                'inner':innerHtml,
                        }
                        return context
                except:
                        return ''

             
@login_required(redirect_field_name="")
def pagos(request):
        try:    
                if request.user.is_superuser:        
                        if request.method == 'GET':
                                lista=lista_tecnicos()
                                # lista=''
                                context={
                                        'lista_tecnicos':lista['inner'],
                                        }
                                return render(request, 'pages/pagos.html', context)
                        else:
                                context={
                                        }
                                return render(request, 'pages/pagos.html', context)
        except:
                context={
                        }
                return render(request, 'pages/pagos.html', context)
