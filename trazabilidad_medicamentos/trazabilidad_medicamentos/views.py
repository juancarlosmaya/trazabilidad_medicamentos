from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def inicio(request):
    #User.objects.get(pk=request.user.id)):
    return render(request,"pagina_inicio.html")


def inventario(request):
    return HttpResponse("hola")
    ##return render(request,"base.html")

def login(request):
    return HttpResponse("hola2")
    ##return render(request,"base.html")
