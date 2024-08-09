from django.db import models

# Create your models here.

class medicamento(models.Model):
    
    cantidad                  = models.DecimalField(decimal_places=0,max_digits=11,null=False,blank= False,default=0)
    
    denominacion              = models.CharField(max_length=50)
    precentacion_farmaceutica = models.CharField(max_length=30, choices = [('FRASCO', 'FRASCO'),('VIAL', 'VIAL'),('AMPOLLA', 'AMPOLLA'),('BLISTER', 'BLISTER'),('JERINGA', 'JERINGA PRELLENA')] ,default='BLISTER') 
    forma_farmaceutica        = models.CharField(max_length=30, choices = [('TABLETA', 'TABLETA'),('CAPSULA', 'CAPSULA'),('SUSPENSION', 'SUSPENSION'),('INYECTABLE', 'SOLUCION INYECTABLE')],default='TABLETA') 
    dosis                     = models.CharField(max_length=20,null=True,blank=True)
    ##unidad_dosis              = models.CharField(max_length=3, choices = [('TR1', 'TR1'),('TR2', 'TR2'),('TR3', 'TR3'),('TR4', 'TR4'),('TR5', 'TR5')],default='TR1') 
    reg_sanitario             = models.CharField(max_length=50)
    lote                      = models.CharField(max_length=50)
    via_administración        = models.CharField(max_length=30, choices = [('ORAL', 'ORAL'),('INTRAVENOSA', 'INTRAVENOSA'),('TOPICA', 'TOPICA,'),('SUBLINGUAL', 'SUBLINGUAL'),('VAGINAL', 'VAGINAL'),('PARENTERAL', 'PARENTERAL'),('INTRAMUSCULAR', 'INTRAMUSCULAR'),('NASAL', 'NASAL'),('OFTALMICA','OFTALMICA'),('OTICA','OTICA')],default='oral') 
    fecha_vencimiento         = models.DateField(default='2025-04-09')
    unidades_empaque          = models.DecimalField(decimal_places=0,max_digits=3,default=1,null=True,blank=True)
    Laboratorio_fabricante    = models.CharField(max_length=50)
    historial                 = models.JSONField(default=dict,null=True,blank=True)
    
    ##models.DurationField(null=True, blank=True)
    def __str__(self):
        return self.denominacion
    
    
    ##def terapias_pendientes(self):
    ##    return self.numero_terapias-self.terapias_realizadas