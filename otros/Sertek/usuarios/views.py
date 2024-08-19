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

@login_required(redirect_field_name="")
def usuarios(request):
        if request.user.is_superuser:             
                if request.method == 'GET':
                        try:       
                                User = get_user_model()
                                users = User.objects.all()
                                
                                # for i in range(0,len(users)):
                                        # print(users[i].username)
                                
                                # print(users[0].get_full_name())
                                u=User.objects.get(username=str(users[1]))
                                print(u.groups)
                                # print(u.userprofile.identidad)
                                


                                context= {
                                        }
                                return render(request, 'pages/usuarios.html', context)                                         

                        except:
                                context= {
                                        }
                                return render(request, 'pages/usuarios.html', context)
                

                       

