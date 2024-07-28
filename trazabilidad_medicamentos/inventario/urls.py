from django.urls import path
from .views import inventario


urlpatterns=[
    path('',inventario)
]