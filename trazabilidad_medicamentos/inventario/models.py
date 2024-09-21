from django.db import models
import csv
from simple_history.models import HistoricalRecords
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
from simple_history import register
from django.contrib.auth.models import User

register(User)


def via_administracion_choices():
    choices = []
    with open('inventario/TablaReferencia_ViaAdministracion__1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter= ';')
        for row in reader:
            choices.append((row[1], row[2]))
    return choices

def forma_farmaceuitica_choices():
    choices = []
    with open('inventario/TablaReferencia_FormaFarmeceutica__1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile,delimiter= ';')
        for row in reader:
            choices.append((row[1], row[2]))
    return choices


# Create your models here.
class Via_administracion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Forma_farmaceutica(models.Model):
    via_administracion = models.ManyToManyField(Via_administracion)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

    
class medicamento(models.Model):
    
    cantidad                  = models.DecimalField(decimal_places=0,max_digits=11,null=False,blank= False,default=0)
    
    denominacion              = models.CharField(max_length=50)
    precentacion_farmaceutica = models.CharField(max_length=30, choices = [('FRASCO', 'FRASCO'),('VIAL', 'VIAL'),('AMPOLLA', 'AMPOLLA'),('BLISTER', 'BLISTER'),('JERINGA', 'JERINGA PRELLENA')] ,default='BLISTER') 
    #forma_farmaceutica        = models.CharField(max_length=30, choices = forma_farmaceuitica_choices(),default='TN') 
    nueva_forma_farmaceutica  =  ChainedForeignKey(
        Forma_farmaceutica,
        chained_field="nueva_via_administracion",
        chained_model_field="via_administracion",
        show_all=False,
        auto_choose=False,
        sort=True)
    dosis                     = models.CharField(max_length=20,null=True,blank=True)
    ##unidad_dosis              = models.CharField(max_length=3, choices = [('TR1', 'TR1'),('TR2', 'TR2'),('TR3', 'TR3'),('TR4', 'TR4'),('TR5', 'TR5')],default='TR1') 
    reg_sanitario             = models.CharField(max_length=50)
    lote                      = models.CharField(max_length=50)
    nueva_via_administracion  = models.ForeignKey(Via_administracion,on_delete=models.CASCADE)
    #via_administración        = models.CharField(max_length=50, choices=via_administracion_choices(),default='PO') 
    fecha_vencimiento         = models.DateField(default='2025-04-09')
    unidades_empaque          = models.DecimalField(decimal_places=0,max_digits=3,default=1,null=True,blank=True)
    Laboratorio_fabricante    = models.CharField(max_length=50)
    historial                 = HistoricalRecords()
    
    ##models.DurationField(null=True, blank=True)
    def __str__(self):
        return self.denominacion
    
    
    ##def terapias_pendientes(self):
    ##    return self.numero_terapias-self.terapias_realizadas

# Create your models here.
class Continent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Country(models.Model):
    continent = models.ManyToManyField(Continent, blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    new_continent = models.ForeignKey(Continent,on_delete=models.CASCADE)
    new_country = ChainedForeignKey(
        Country,
        chained_field="new_continent",
        chained_model_field="continent",)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)

    def __str__(self):
        return self.city
