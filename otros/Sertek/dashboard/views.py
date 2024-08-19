from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
import math
# from datetime import date
import datetime
from django.contrib.auth.decorators import login_required
from usuarios import models

from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]

# Create your views here.

# Consulta todos los servicios con distintos estados
def carga_dashboard(user):       
        lista_estados=config.config.lista_estados
        # print(lista_estados)
        
        summary=[]
        summary_aux=[]
        for i in range(0,len(lista_estados)):
                # print(lista_estados[i])
                # print(user.lugar)
                summary_aux.append(lista_estados[i])
                if user.lugar!='Colombia':
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+'tipo'+'=='+'servicio'+';'+'ultimo_estado'+'~='+str(lista_estados[i])+';'+'sede'+'=='+str(user.lugar)+'&limit=1000&options=count'
                else:
                       url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+'tipo'+'=='+'servicio'+';'+'ultimo_estado'+'~='+str(lista_estados[i])+'&limit=1000&options=count'
                headers={"Accept":"application/json"}   
                response=requests.get(url,headers=headers)
                if (response.status_code==200):
                        rh = json.dumps(response.headers.__dict__['_store'])
                        response_JSON=json.loads(rh)
                        # print(response_JSON)
                        total_id=int(response_JSON['fiware-total-count'][1])
                        summary_aux.append(total_id)
                        summary.append(summary_aux)
                        summary_aux=[]
                        # print(total_id)
                        # if (total_id!=0):    
                        #         dict_entidades=response.content.decode("utf-8").replace("'", '"')
                        #         dict_entidades=json.loads(dict_entidades)
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
                                # return total_id,dict_entidades
                                # print()
                        # else:
                        #         dict_identidades=None
                        #         return total_id,dict_identidades
        # print(summary)
        return summary            

            

# Consulta todos los servicios sin asignar
def consulta_servicios_sin_asignar(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3,atributo_4,valor_4):
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    if valor_4!='Colombia':
        if (valor_3==''):
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+';'+atributo_4+'=='+valor_4+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
        else:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+';'+atributo_3+'~='+valor_3+';'+atributo_4+'=='+valor_4+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
                headers={"Accept":"application/json"}
    else:
        if (valor_3==''):
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'=='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
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

                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))

                        total_enity,dict_entity=consulta_servicios_sin_asignar(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo','servicio','asignar',asigna,atributo,search,'sede',u.lugar)
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_servicios_sin_asignar(int(por_pagina),0,'tipo','servicio','asignar',asigna,atributo,search,'sede',u.lugar)
                                actual_page=1

                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        innerHtml=""

                        # print(dict_entity[1]['fecha']['value'])
                        # print(type(dict_entity[1]['fecha']['value']))

                        for i in range(0,len(dict_entity)):
                                # Calculamos la diferencia de días desde la creación
                                date_now=datetime.datetime.now()
                                date_format = '%Y-%m-%d'
                                # print(dict_entity[i]['fecha']['value'])
                                # print(type(dict_entity[i]['fecha']['value']))
                                date_0 = datetime.datetime.strptime(dict_entity[i]['fecha']['value'].split('T')[0], date_format)
                                diff=date_now-date_0

                                innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1_servicios">'+str(dict_entity[i]['id'])+'</td>'  + '<td class="th2_servicios">'+str(dict_entity[i]['tipo_servicio']['value'])+'</td>' + '<td class="th3_servicios">'+str(dict_entity[i]['producto']['value'])+'</td>' + '<td class="th4_servicios">'+str(dict_entity[i]['marca']['value'])+'</td>' + '<td class="th7_servicios">'+str(diff.days)+'</td>' + '<td class="th6_servicios">'+str(dict_entity[i]['direccion']['value'])+'</td>'+ '<td class="th6_servicios">'+str(dict_entity[i]['tecnico']['value'])+'</td>' + '<td class="th7_servicios"> </ion-icon> <ion-icon class="select_cliente" name="eye-outline" onclick="ver_servicio('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'                  
                                
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
def dashboard(request):
        try:         
                if request.method == 'GET':
                        # 0  'Carga de trabajo',
                        # 1  'Sin asignar',
                        # 2  'Asignar estado',
                        # 3  'Sin asignación',
                        # 4  'Repuesto disponible en CSA',
                        # 5  'Pendiente por repuesto',
                        # 6  'Pendiente por aprobación de cliente',
                        # 7  'Proceso de cambio',
                        # 8  'Proceso de reparación',
                        # 9  'Proceso de reparación en taller',
                        # 10 'Producto en proceso de cambio',
                        # 11 'Producto entregado',
                        # 12 'Producto reparado',
                        # 13 'Servicio cancelado',
                        # 14 'Soporte técnico'
                        resultados_dashboard=carga_dashboard(models.UserProfile.objects.get(user__username=str(request.user.username)))
                        # Total ordenes= Sumatoria menos las que tienen el estado Producto entregado
                        total_ordenes=0
                        for i in range(0,len(resultados_dashboard)):
                                if i != 11:
                                        total_ordenes=total_ordenes+resultados_dashboard[i][1]
                        print('Total odenes abiertas ',total_ordenes)
                        context={
                                'carga_de_trabajo': resultados_dashboard[0][1],
                                'pendiente_por_repuesto': resultados_dashboard[5][1],
                                'soporte_tecnico': resultados_dashboard[14][1],
                                'proceso_de_cambio': resultados_dashboard[7][1],
                                'producto_entregado': resultados_dashboard[11][1],
                                'total_ordenes': total_ordenes,
                                }
                        return render(request, 'pages/dashboard.html', context)
                else:
                        context={
                        }
                        return render(request, 'pages/dashboard.html', context)
        except:
                context={
                        }
                return render(request, 'pages/dashboard.html', context)