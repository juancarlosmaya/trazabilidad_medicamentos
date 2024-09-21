from django import forms
from .models import medicamento, Location, Forma_farmaceutica,Via_administracion
from django.contrib.admin.widgets import AdminDateWidget
from smart_selects import form_fields


class formularioMedicamento(forms.ModelForm):
    
    class Meta:
        model = medicamento
        
        #nueva_via_administracion = forms.ModelChoiceField(queryset= Via_administracion.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
        #nueva_forma_farmaceutica = forms.ModelChoiceField(queryset= Forma_farmaceutica.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

        fields= ['cantidad', 'denominacion', 'nueva_via_administracion', 'nueva_forma_farmaceutica', 'dosis','reg_sanitario','lote','fecha_vencimiento','unidades_empaque','Laboratorio_fabricante']
       
        widgets = {
            'cantidad' : forms.NumberInput(attrs={'class':'form-control'}),
            'denominacion' : forms.TextInput(attrs={'class':'form-control'}),
        #    'precentacion_farmaceutica' : forms.Select(attrs={'class':'form-control'}),
        #    'forma_farmaceutica' : forms.Select(attrs={'class':'form-control'}),
            'dosis': forms.TextInput(attrs={'class':'form-control'}),
            'reg_sanitario' : forms.TextInput(attrs={'class':'form-control'}),
            'lote' : forms.TextInput(attrs={'class':'form-control'}),
        #    'nueva_via_administración' : forms.ModelChoiceField(queryset= Via_administracion.objects.all(),attrs={'class':'form-control'}),
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
    
    
    cantidadDispensar = forms.CharField(label="Cantidad a Retirar", max_length=100, widget= forms.NumberInput(attrs={'class':'form-control'}))


class formularioLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['new_continent','new_country','city','street']
