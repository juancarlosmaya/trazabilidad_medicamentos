from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import medicamento
from .forms import formularioMedicamento
# Create your views here.

def inventario(request):
    medicamentos = medicamento.objects.all()
    return render(request,'inventario/inventario.html',{'medicamentos':medicamentos})


def nuevo_medicamento(request):
    if request.method=="POST":
        mi_formulario=formularioMedicamento(request.POST)
        if mi_formulario.is_valid():
            ##mi_formulario_edicion = mi_formulario.save(commit=False)
            ##mi_formulario_edicion.numero_terapias=10
            ##mi_formulario_edicion.terapias_realizadas=0
            ##mi_formulario_edicion.save()
            mi_formulario.save()
            print('Nuevo paciente guardado')
            return redirect('inventario')
        else:
            print('Datos de nuevo paciente no son validos')
    else:
        ##'denominacion', 'precentacion_farmaceutica', 'forma_farmaceutica', 'dosis','reg_sanitario','lote','via_administración','fecha_vencimiento','unidades_empaque','Laboratorio_fabricante','historial']
        mi_formulario= formularioMedicamento(initial={'cantidad': '3','dosis':'100 MG'})
        return render(request,'inventario/nuevo_medicamento.html',{'mi_formulario':mi_formulario})
