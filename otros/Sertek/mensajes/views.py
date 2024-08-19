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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

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

@login_required(redirect_field_name="")
def get_global_message(request):
        try:
            entidad_global_message=consulta_entidad('global_message')  
            # print(entidad_global_message['global_message']['value'])  
            context={
                    'global_message':entidad_global_message['global_message']['value'],
                    }
            return JsonResponse(context,  safe=False)
        except:
            context={
                'global_message':'                                 ',
                }
            return JsonResponse(context,  safe=False)

@login_required(redirect_field_name="")
def set_global_message(request):
   if request.user.is_superuser: 
        try:
            # Actualiza campo de mensaje global
            mensaje_global = request.GET.get('mensaje_global',"")
        #     print(mensaje_global)
            mensaje_global= str(request.user.username)+' dice: '+mensaje_global
            ContextDataJSON={"global_message": {
                        "value": str(mensaje_global),
                        "type": "String"
                        }
                        }
        #     url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+'global_message'+'/attrs/'+'global_message'+'/value'
            url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+'global_message'+'/attrs/'
        #     headers={"Content-Type":"text/plain"}   
        #     headers={"Content-Type":"text/plain"}   
            headers={"Accept":"application/json"}      
            response=requests.put(url,headers=headers,json=ContextDataJSON)
            if (response.status_code) == 204:
                context={
                        'message':'El mensaje fue publicado.',
                }
                return JsonResponse(context,  safe=False)
            else :
                context={
                        'message':'El mensaje NO fue publicado.',
                }
                return JsonResponse(context,  safe=False)

            
        except:
            context={
                'message':'El mensaje NO fue publicado.',
                }
            return JsonResponse(context,  safe=False)

   else:
        context={
        'message':'El usuario no tiene los permisos ncesarios para realizar esta acción.',
        }
        return JsonResponse(context,  safe=False)
         

@login_required(redirect_field_name="")
def mensajes(request):
        if request.user.is_superuser:             
                if request.method == 'GET':
                        try:       
                                # User = get_user_model()
                                # users = User.objects.all()
                                
                                # # for i in range(0,len(users)):
                                #         # print(users[i].username)
                                
                                # # print(users[0].get_full_name())
                                # u=User.objects.get(username=str(users[1]))
                                # print(u.groups)
                                # # print(u.userprofile.identidad)
                                


                                context= {
                                        }
                                return render(request, 'pages/mensajes.html', context)                                         

                        except:
                                context= {
                                        }
                                return render(request, 'pages/mensajes.html', context)
        else:
                return render(request, 'pages/error.html', context) 
                


