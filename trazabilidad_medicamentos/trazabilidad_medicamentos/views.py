from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    return render(request,"base.html")

def inventario(request):
    return HttpResponse("hola")
    ##return render(request,"base.html")

def login(request):
    return HttpResponse("hola2")
    ##return render(request,"base.html")
