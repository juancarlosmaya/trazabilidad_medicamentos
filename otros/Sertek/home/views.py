from django.shortcuts import render
from django.template import Template
from django.http import HttpRequest as request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse
from usuarios import models


@login_required(redirect_field_name="")
def cambio_ciudad(request):
        u=models.UserProfile.objects.get(user__username=str(request.user.username))
        if u.cambio_ciudad==True:
                try:     
                        ciudad = request.GET.get('ciudad','')  
                        # u=User.objects.get(username=str(request.user.username))
                        # u=User.objects.get(username=str(request.user.username))
                        # profile=models.UserProfile.identidad
                        # print(profile)

                        # u.userprofile.realiza_servicio = True
                        # u.email = 'asd@asd.com' 
                        # u.userprofile.identidad = '7777'
                        u=models.UserProfile.objects.get(user__username=str(request.user.username))
                        # u.identidad = '777766'
                        u.lugar = str(ciudad)
                        u.save()
                        context= {
                                'message':"Cambio de ciudad realizado ",
                        }
                        return JsonResponse(context)
                
                except:
                        context= {
                                'message':" No fue posible cambioar de ciudad",
                        }
                        return JsonResponse(context)
        else:
                context= {
                        'message':" No tiene los permisos para realizar esta acción",
                }
                return JsonResponse(context)

@login_required(redirect_field_name="")
def ciudad_actual(request):
        u=User.objects.get(username=str(request.user.username))
        lista=models.UserProfile.lugar_lista
        innerHtml=''
        for i in range(0,len(lista)):
                if u.userprofile.lugar!=str(lista[i][1]):                                   
                        innerHtml=innerHtml+ '<option  value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'                                                      
                else:
                        innerHtml=innerHtml+ '<option selected value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'     

        context= {
                'lista_ciudades':innerHtml,
        }
        # username = request.user.username
        return JsonResponse(context)
        # return redirect("/home")

@login_required(redirect_field_name="")
def home(request):
        u=User.objects.get(username=str(request.user.username))
        lista=models.UserProfile.lugar_lista
        innerHtml=''
        for i in range(0,len(lista)):
                if u.userprofile.lugar!=str(lista[i][1]):                                   
                        innerHtml=innerHtml+ '<option  value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'                                                      
                else:
                        innerHtml=innerHtml+ '<option selected value="'+str(lista[i][0])+'">'+str(lista[i][1])+'</option>'     

        context= {
                'lista_ciudades':innerHtml,
        }
        # username = request.user.username
        return render(request, 'pages/home.html',context)
        # return redirect("/home")
