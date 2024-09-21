from django.urls import path,include,re_path
from .views import inventario,nuevo_medicamento,dispensar_medicamento,historial_medicamento,funcionLocation


urlpatterns=[
    path('',inventario,name='inventario'),
    path('nuevo',nuevo_medicamento,name='nuevo'),
    path('dispensar/<int:medicamento_id>/',dispensar_medicamento,name='dispensar'),
    path('historial/<int:medicamento_id>/',historial_medicamento,name='historial'),
    re_path(r'^chaining/', include('smart_selects.urls')),
    path('location',funcionLocation)
]