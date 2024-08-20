from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import medicamento
from .forms import formularioMedicamento, formularioDispensar
from django.contrib import messages
import datetime
import json

# Create your views here.

def inventario(request):
    medicamentos = medicamento.objects.all()
    vencimientos= []
    i=0
    for medicamentoExaminar in medicamentos:
        today = datetime.date.today()
        difference =  medicamentoExaminar.fecha_vencimiento - today
        months_difference = difference.days //30   # meses de diferencia
        if months_difference > 8:
            vencimientos.append(0)
        else:
            vencimientos.append(1)
        i = i +1
    print(vencimientos)
    #diccionarioMediccamentos ={item['id']: item for item in medicamentos.values()}
    #print(diccionarioMediccamentos)
    medicamentos_con_vencimiento = zip(medicamentos, vencimientos)
    return render(request,'inventario/inventario.html',{'medicamentos':medicamentos_con_vencimiento})


def nuevo_medicamento(request):
    if request.method=="POST":
        ## si se envían datos de nuevo medicamento, y son validos, son gradados en modelo medicamento
        mi_formulario=formularioMedicamento(request.POST)
        if mi_formulario.is_valid():
            mi_formulario.save()
            print('Nuevo paciente guardado')
            return redirect('inventario')
        else:
            print('Datos de nuevo paciente no son validos')
    else:
        ## despliega el formulario formularioMedicamento con inicialización
        mi_formulario= formularioMedicamento(initial={'cantidad': '3','dosis':'100 MG'})
        return render(request,'inventario/nuevo_medicamento.html',{'mi_formulario':mi_formulario})

def dispensar_medicamento(request, medicamento_id):
    if request.method=="POST":
        ## Si se enviaron los datos de dispensación y son correctos, se resta la dispensación en el modelo medicamento
        mi_formulario=formularioDispensar(request.POST)
        if mi_formulario.is_valid():
            medicamento_dispensar = medicamento.objects.get(pk=medicamento_id)
            print('DISPENSANDO')
            print(mi_formulario.cleaned_data['cantidadDispensar'])
            medicamento_dispensar.cantidad= medicamento_dispensar.cantidad - int(mi_formulario.cleaned_data['cantidadDispensar'])
            medicamento_dispensar.save()
            print('DISPENSADO')
            # mensaje de dispensenación correcta
            messages.success(request, str(medicamento_dispensar) + " dispensado correctamente (" + mi_formulario.cleaned_data['cantidadDispensar'] + " unidades)" ) # mensaje a mostrar en plantilla inventario.html
            return redirect('inventario')
        else:
            print('Errror en dispensación, dato invalido')
    else: 
        ## Obtiene los datos del medicamento a dispensar y los despliega en el formularo formularioDispensar
        medicamento_dispensar = medicamento.objects.get(pk=medicamento_id)
        print("medicamento a dispensar:")
        print(medicamento_dispensar)
        mi_formulario= formularioDispensar(initial={'cantidadDispensar': medicamento_dispensar.cantidad})
        return render(request,'inventario/dispensar.html',{'mi_formulario':mi_formulario,'medicamento':medicamento_dispensar})