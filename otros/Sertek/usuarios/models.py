from django.db import models
from django.contrib.auth.models import User
import datetime



class UserProfile(models.Model):
    rol_choices = [('1','Admin'),('2','Operativo'),('3','Técnico')]
    lugar_lista = [('Bogotá','Bogotá'),('Barranquilla','Barranquilla'),('Medellín','Medellín'),('Colombia','Colombia')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100, choices=rol_choices, default=None)
    lugar = models.CharField(max_length=100, choices=lugar_lista, default=None)
    identidad = models.CharField(max_length=100, blank=True)
    cambio_ciudad=models.BooleanField(default=False)
    realiza_servicio=models.BooleanField(default=False)
    fecha_creacion=models.DateField(default=datetime.datetime.now, editable=True)
    image_profile=models.ImageField(upload_to="static/img/",default="static/img/user_default.png")
    