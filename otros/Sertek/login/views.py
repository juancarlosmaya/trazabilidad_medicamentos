from django.shortcuts import render
from django.template import Template, Context
# import requests
from django.contrib.auth import aauthenticate 
from django.contrib.auth import alogin, alogout
from django.shortcuts import redirect

# from django.contrib.auth import User

from  django.http import HttpRequest as request

from django.contrib.auth.models import UserManager


from django.contrib.auth.models import User

from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]
# Create your views here.


async def login(request):
    if request.method == 'POST':
        
        # submit = request.GET.get('submit')
        username = request.POST['username']
        password = request.POST['password']
        # if (submit is not None):
        if (username is not None) and (password is not None ):
            # return redirect("/home")
            # auser=HttpRequest.auser()
            # await request.auser()
            
            # auser= aauthenticate(username=username,password=password) 
            auser=await aauthenticate(username=username,password=password)

            # User.objects.get(username="fsmith")
            # print( u.employee.department )
            # print(str(auser))
            # print(type(str(auser)))          

            if auser is not None:   
                await alogin(request,auser)   
                # await login         
                context= {
                'message': auser,
                # 'message': password,
                }
                return redirect("/home")
                # alogout(request)
                # return redirect("/home")
                return render(request, 'pages/login.html', context)
            else:
                context= {
                'message': "Nombre de usuario o contraseña incorrecta",
                }
                return render(request, 'pages/login.html', context)

        else:
            context= {
            # 'message': "Nombre de usuario o contraseña incorrecta",
            'message': "Digite su usuario y contraseña",
            #  message.info(request, "invalid credentials")
            }
            return render(request, 'pages/login.html', context)
        # else:
        #     context= {
        #         'message': "Submit is none",
        #         }
        #     return render(request, 'pages/login.html', context)
    else:
        context= {
        # 'message': "Nombre de usuario o contraseña incorrecta",
        'message': "",
        }
        return render(request, 'pages/login.html', context)


