from django.http import HttpResponse
from django.shortcuts import render
from inventario.models import medicamento
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

def historial(request):
    usuario = User.objects.get(pk=request.user.id).get_full_name
    historial_usuario = medicamento.historial.filter(history_user_id=request.user.id)
    return render(request,"historial_usuario.html",{'usuario':usuario,'historial_usuario':historial_usuario})