from django.shortcuts import render
from django.template import Template
from django.http import HttpRequest as request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.paginator import Paginator
import requests
import json
from django.http import JsonResponse
import math
from usuarios import models
from django.contrib.auth.models import User


from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]
# Crea un contacto
# @login_required(redirect_field_name="")
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
                                "value": "contacto",
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
                        return "El contacto ha sido creado"
                if (response.status_code) == 422:
                        return "El contacto ya existe"
                return "El contacto NO pudo ser creado"
        except:
                return "El contacto NO pudo ser creado"

# Actualiza atributo de entidad
# @login_required(redirect_field_name="")
def update(tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email):
        try:    
                ContextDataJSON={"tipo_contacto": {
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

                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(identidad)+'/attrs/'
                headers={"Accept":"application/json"}      
                response=requests.put(url,headers=headers,json=ContextDataJSON)
                # print(response.status_code)
                if (response.status_code) == 204:
                        return "El contacto ha sido actualizado"
                else :
                        return "El contacto NO pudo ser actualizado"

        except:
                return "El contacto NO pudo ser actualizado"

# Consulta una entidades por atributo
# @login_required(redirect_field_name="")
def consulta_entiti_atributo(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3):
    # url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'~='+valor+'&limit='+str(paginado)+'&options=count'
    # url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+'&limit='+str(paginado)+'&options=count'
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'~='+valor_3+'&limit='+str(paginado)+'&options=count'
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        print(response)
        if (response.status_code==200):
            try:
                rh = json.dumps(response.headers.__dict__['_store'])
                response_JSON=json.loads(rh)
                total_id=int(response_JSON['fiware-total-count'][1])
                # print(total_id)  # Número de resgistros encontrados
                if (total_id!=0):    
                    # print(response.content)
                    # dict_identidades=response.content.json()
                    dict_entidades=response.content.decode("utf-8").replace("'", '"')
                    # print(dict_entidades)
                    dict_entidades=json.loads(dict_entidades)
                    while(total_id>len(dict_entidades)):
                        print("hace")
                        # offset_aux=len(dict_entidades)+offset_aux
                        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'~='+valor_3+'&limit='+str(paginado)+'&options=count&offset='+str(len(dict_entidades))
                        headers={"Accept":"application/json"}
                        response=requests.get(url,headers=headers)
                        # print(response)
                        dict_entidades_aux=response.content.decode("utf-8").replace("'", '"')
                        dict_entidades_aux=json.loads(dict_entidades_aux)
                        dict_entidades=dict_entidades+dict_entidades_aux
                    # print(type(dict_entidades))
                    # print(dict_identidades[0]['identidad']['value'])
                    
                    # for enity in dict_entidades:
                        # print(enity['id'])
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

# Elimina entidad
# @login_required(redirect_field_name="")
def borra_entidad(id_entyti):
        try:
                url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+str(id_entyti)
                headers={"Accept":"application/json"}
                response=requests.delete(url,headers=headers)
                if (response.status_code) == 204:
                        return "El contacto ha sido eliminado"
                else :
                        return "El contacto NO pudo ser eliminado"
        except:
               return "El contacto NO pudo ser eliminado, error en la base de datos"


# Consulta todos los servicios sin asignar
# @login_required(redirect_field_name="")
def consulta_contactos(paginado,offset,atributo,valor,atributo_2,valor_2,atributo_3,valor_3):
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
#     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    if valor_3!='Colombia':
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+';'+atributo_3+'=='+valor_3+'&limit='+str(paginado)+'&options=count&offset='+str(offset)
    else:
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+';'+atributo_2+'~='+valor_2+'&limit='+str(paginado)+'&options=count&offset='+str(offset)   
    headers={"Accept":"application/json"}
    try:
        response=requests.get(url,headers=headers)
        print(response.status_code)
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
def cliente_proveedor(request):                    
        if request.method == 'GET':
                try:     
                        # Extraemos el perfil
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        if u.cambio_ciudad==True:
                                lista=models.UserProfile.lugar_lista # Va por la lista de ciudad del MOdels usuarios
                                innerHtml='<option value="" disabled selected hidden>Sede</option>'                        
                                for i in range(0,len(lista)):                                 
                                                innerHtml=innerHtml+ '<option  value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'                                                      
                                context= {
                                        'lista_ciudades':innerHtml ,
                                        }
                                return render(request, 'pages/cliente_proveedor.html', context) 
                        else:  
                                context= {
                                        'lista_ciudades':'<option  value="'+str(u.lugar)+'">'+str(u.lugar)+'</option>'  ,
                                        }
                                return render(request, 'pages/cliente_proveedor.html', context)                                       

                except:
                        context= {
                                }
                        return render(request, 'pages/cliente_proveedor.html', context)

@login_required(redirect_field_name="")               
def crear_contacto(request):
        # Busca un modelo                            
        if request.method == 'GET':
                try:    
                        tipo_contacto = request.GET.get('tipo_contacto',"")
                        tipo_identidad = request.GET.get('tipo_identidad',"")
                        identidad = request.GET.get('identidad',"")
                        nombre = request.GET.get('nombre',"")
                        direccion = request.GET.get('direccion',"")
                        telefono = request.GET.get('telefono',"")
                        departamento = request.GET.get('departamento',"")
                        localidad = request.GET.get('localidad',"")
                        email = request.GET.get('email',"")                 
                        message=crea_contacto(tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email)
                        print("crea contacto")
                        context= {
                                'message': message,
                                }
                        return JsonResponse(context)
                except:
                        context= {
                                'message': None,
                                }
                        return JsonResponse(context)

@login_required(redirect_field_name="")               
def busca_contactos(request):
        # Busca contacto                                                    
        if request.method == 'GET':
                try:    
                        search = request.GET.get('search',"")
                        por_pagina = request.GET.get('por_pagina',"")
                        actual_page = request.GET.get('actual_page',"")
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        total_enity,dict_entity=consulta_contactos(int(por_pagina),((int(actual_page)-1)*int(por_pagina)),'tipo','contacto','identidad',search,'departamento',u.lugar)
                        if (len(dict_entity)==0) and (actual_page!='1'):
                                total_enity,dict_entity=consulta_contactos(int(por_pagina),0,'tipo','contacto','identidad','0','departamento',u.lugar)
                                actual_page=1
                        # print(type(dict_entity))
                        num_pages=math.ceil(int(total_enity)/int(por_pagina))
                        innerHtml=""
                        for i in range(0,len(dict_entity)):
                                innerHtml=innerHtml+ '<tr class="filas_tabla">' + '<td class="th1">'+str(dict_entity[i]['tipo_identidad']['value'])+'</td>'  + '<td class="th2">'+str(dict_entity[i]['tipo_contacto']['value'])+'</td>' + '<td class="th3">'+str(dict_entity[i]['identidad']['value'])+'</td>' + '<td class="th4">'+str(dict_entity[i]['nombre']['value'])+'</td>' + '<td class="th5">'+str(dict_entity[i]['telefono']['value'])+'</td>' + '<td class="th6">'+str(dict_entity[i]['email']['value'])+'</td>' + '</td>' + '<td class="th7">'+str(dict_entity[i]['localidad']['value'])+'</td>' + '<td class="th8"> <ion-icon class="pencil" name="pencil-outline" onclick="openmodal_edit('+str(dict_entity[i])+')"> </ion-icon> <ion-icon class="basurero" name="trash-outline" onclick="openmodal_delete('+str(dict_entity[i])+')"></ion-icon></td>' +'</tr>'                  
                                
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
                
@login_required(redirect_field_name="")
# @user_passes_test(lambda u: u.is_superuser)
def eliminar_contacto(request):
        if request.user.is_superuser:
                if request.method == 'GET':
                        try:
                                entity = request.GET.get('entity',"")
                                orion_request=borra_entidad(str(entity))
                                context= {
                                        'message':orion_request,
                                }
                                return JsonResponse(context)
                        except:
                                context= {
                                        'message':"",
                                }
                                return JsonResponse(context)
        else:
                context= {
                        'message':"No tiene los permisos para realizar esta acción",
                }
                return JsonResponse(context)
                
@login_required(redirect_field_name="")               
def editar_contacto(request):
       if request.method == 'GET':
                try:
                        tipo_contacto = request.GET.get('tipo_contacto',"")
                        tipo_identidad = request.GET.get('tipo_identidad',"")
                        identidad = request.GET.get('identidad',"")
                        nombre = request.GET.get('nombre',"")
                        direccion = request.GET.get('direccion',"")
                        telefono = request.GET.get('telefono',"")
                        departamento = request.GET.get('departamento',"")
                        localidad = request.GET.get('localidad',"")
                        email = request.GET.get('email',"")    
                        orion_request=update(tipo_contacto, tipo_identidad, identidad, nombre, direccion, telefono, departamento, localidad, email)

                        context= {
                                'message':orion_request,
                        }
                        return JsonResponse(context)
                except:
                        context= {
                                'message':"",
                        }
                        return JsonResponse(context)
                       

