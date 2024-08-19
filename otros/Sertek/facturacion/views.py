from django.shortcuts import render
from django.template import Template
from django.http import HttpRequest as request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
import requests
import json
from django.http import JsonResponse
import math
from usuarios import models


from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]


# Consulta todos los remisiones 
def consulta_remisiones(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3,atributo_4,valor_4):
    if (valor_3=='true'):
           valor_3=1
    else:
           valor_3=0
#     print(valor_3)
#     print(atributo_3)
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    if valor_4!='Colombia':
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'=='+str(valor_3)+';'+atributo_4+'=='+str(valor_4)+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    else:
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'=='+str(valor_3)+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    headers={"Accept":"application/json"}
    
    try:
        response=requests.get(url,headers=headers)
        # print(response.status_code)
        print('asdds')
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
def facturacion_remision(request):
                    
        if request.method == 'GET':
                try:       
                        context= {
                                }
                        return render(request, 'pages/facturacion_remision.html', context)                                         

                except:
                        context= {
                                }
                        return render(request, 'pages/facturacion_remision.html', context)
                


@login_required(redirect_field_name="")                 
def busca_remision(request):
        # Busca contacto                                                    
        if request.method == 'GET':
                try:    
                        search = request.GET.get('search',"")
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")
                        activa = request.GET.get('activa','false') 
                        
                        # Extraemos perfil
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        

                        total_enity,dict_entity=consulta_remisiones(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo','remision','remision',search,'activa',activa,'sede',u.lugar)
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_remisiones(int(por_pagina),0,'tipo','remision','tipo','remision','activa',activa,'sede',u.lugar)
                                actual_page=1
                        # print(type(dict_entity))
                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        innerHtml=""
                        for i in range(0,len(dict_entity)):
                                innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1">'+str(dict_entity[i]['remision']['value'].split('_')[-1])+'</td>'  + '<td class="th2">'+'Preguntar'+'</td>' + '<td class="th3">'+str(dict_entity[i]['fecha_creacion']['value'].split('T')[0])+'</td>' + '<td class="th4">'+str(dict_entity[i]['medio_pago']['value'])+'</td>' + '<td class="th5">'+str(dict_entity[i]['servicio']['value'])+'</td>' + '<td class="th6">'+str(dict_entity[i]['cliente']['value'])+'</td>' + '</td>' + '<td class="th7">'+str(dict_entity[i]['total']['value'])+'</td>' + '<td class="th8"> <ion-icon class="pencil" name="eye-outline" onclick="ver_servicio('+str(dict_entity[i]['servicio']['value'])+')"> </ion-icon> <ion-icon class="basurero" name="trash-outline" onclick="openmodal_delete('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'                  
                                
                        context= {
                                'inner':innerHtml,
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



def agrega_corrdenadas(request):                                                 
        if request.method == 'GET':
                try:    
                        longitud = request.GET.get('longitud',"")
                        latitud = request.GET.get('latitud',"")
                                                         
                        if longitud!='' and latitud!='':
                                context= {
                                        'mensaje':'Las coordenadas se registraron de manera satisfactoria',

                                }
                                return JsonResponse(context)
                        else:
                                context= {
                                        'mensaje':'Las coordenadas NO se registraron de manera satisfactoria',

                                }
                                return JsonResponse(context)
                except:
                        context= {
                                'mensaje':"Error en la función agrega_corrdenadas ",
                        }
                        return JsonResponse(context)

                
                       

