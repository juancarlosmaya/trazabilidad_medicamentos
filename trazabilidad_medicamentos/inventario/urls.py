from django.urls import path
from .views import inventario,nuevo_medicamento


urlpatterns=[
    path('',inventario,name='inventario'),
    path('nuevo',nuevo_medicamento,name='nuevo')
]