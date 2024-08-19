from django import forms
from .models import medicamento
from django.contrib.admin.widgets import AdminDateWidget

class formularioMedicamento(forms.ModelForm):
    
    class Meta:
        model = medicamento
        #fields= ['nombre', 'cedula', 'fecha_nacimiento', 'terapia', 'numero_terapias', 'terapias_realizadas']
        fields= ['cantidad', 'denominacion', 'precentacion_farmaceutica', 'forma_farmaceutica', 'dosis','reg_sanitario','lote','via_administración','fecha_vencimiento','unidades_empaque','Laboratorio_fabricante']


        
        labels = {
        "esperaEntreTerapias": "Tiempo de entre terapias"
        }
        
        # initials ={
        #     'fecha_nacimiento':datetime.date(1980, 5, 17),
        # }
        
        widgets = {
            'cantidad' : forms.NumberInput(attrs={'class':'form-control'}),
            'denominacion' : forms.TextInput(attrs={'class':'form-control'}),
            'precentacion_farmaceutica' : forms.Select(attrs={'class':'form-control'}),
            'forma_farmaceutica' : forms.Select(attrs={'class':'form-control'}),
            'dosis': forms.TextInput(attrs={'class':'form-control'}),
            'reg_sanitario' : forms.TextInput(attrs={'class':'form-control'}),
            'lote' : forms.TextInput(attrs={'class':'form-control'}),
            'via_administración' : forms.Select(attrs={'class':'form-control'}),
            #'fecha_vencimiento' : forms.DateInput(format='%m/%d/%Y', attrs={'class':'form-control datepicker',  'autocomplete': 'on'}),
            'fecha_vencimiento' :forms.DateInput(attrs=dict(type='date')),
            'unidades_empaque' : forms.NumberInput(attrs={'class':'form-control'}),
            'Laboratorio_fabricante' : forms.TextInput(attrs={'class':'form-control'})           
        }

        def __init__(self, *args, **kwargs):
            # first call parent's constructor
            super(formularioMedicamento, self).__init__(*args, **kwargs)
            # there's a `fields` property now
            self.fields['historial'].required = False
            


class formularioDispensar(forms.Form):
    
    
    cantidadDispensar = forms.CharField(label="Cantidad a dispensar", max_length=100, widget= forms.NumberInput(attrs={'class':'form-control'}))


