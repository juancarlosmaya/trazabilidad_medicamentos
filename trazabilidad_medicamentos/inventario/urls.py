from django.urls import path
from .views import inventario,nuevo_medicamento,dispensar_medicamento


urlpatterns=[
    path('',inventario,name='inventario'),
    path('nuevo',nuevo_medicamento,name='nuevo'),
    path('dispensar/<int:medicamento_id>/',dispensar_medicamento,name='dispensar')
]