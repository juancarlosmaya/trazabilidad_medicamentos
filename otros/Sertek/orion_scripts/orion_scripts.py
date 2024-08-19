# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 23:37:21 2024

@author: Lennin Escobar
"""

import requests
import json
import os

IP_Orion="192.168.43.173"
# IP_Orion="192.168.10.167"
Port_Orion="1026"

# Get version
def version():
    url='http://'+IP_Orion+':'+Port_Orion+'/version'
    # headers={"Content-Type":"text/plain"}
    response=requests.get(url)
    print(response.status_code)
    print(response.content) 
    
# Consulta una entidad específica
def consulta_entiti(entidad):
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+entidad
    headers={"Accept":"application/json"}
    response=requests.get(url,headers=headers)
    print(response.status_code)
    response=response.content.decode("utf-8").replace("'", '"')
    response_JSON=json.loads(response)
    print(response_JSON)

# Consulta una entidades por atributo
def consulta_entiti_atributo(atributo,valor):
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities?q='+atributo+'=='+valor+'&limit=1&options=count'
    headers={"Accept":"application/json"}
    response=requests.get(url,headers=headers)
    print(response.status_code)
    print(response.headers )
    response=response.content.decode("utf-8").replace("'", '"')
    response_JSON=json.loads(response)
    print(response_JSON)
    
# Consulta todas las entidades
def todas_entidades():
    url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
    headers={"Accept":"application/json"}
    response=requests.get(url,headers=headers)
    print(response.status_code)
    print(response.content) 
    
# Consulta login - usuario y contraseña
# Esta función retorna el password de un usuario cedula-password
def login_get_password(cedula):
    try:
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+cedula
        headers={"Accept":"application/json"}
        response=requests.get(url,headers=headers)
        print(response.status_code)
        if response.status_code == 200 :
            response=response.content.decode("utf-8").replace("'", '"')
            response_JSON=json.loads(response)
            # print(response_JSON)
            get_pass=response_JSON['password']['value']
            print('El password es',get_pass)
            # print(type(get_pas))
            return get_pass
        if response.status_code == 404 :
            print("el usuario no existe")
            return "el usuario no existe"
        
    except:
        return "Error funcion login_get_password from orion_funciones"
    
    
# Crea un cliente
def crea_cliente(Nombre,Ciudad,Dirección,Cédula,Telefono):
        ContextData=open('orion_cliente.json')
       # print(ContextData)
        ContextDataJSON=json.load(ContextData)
        ContextDataJSON['id']=Cédula
        ContextDataJSON['type']='Cliente'  
        ContextDataJSON['Nombre']['value']=Nombre        
        ContextDataJSON['Ciudad']['value']=Ciudad
        ContextDataJSON['Direccion']['value']=Dirección 
        ContextDataJSON['Cedula']['value']=Cédula 
        ContextDataJSON['Telefono']['value']=Telefono 
        ContextDataJSON['Tipo']['value']=Telefono 
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
        headers={"Accept":"application/json"}
        response=requests.post(url,headers=headers,json=ContextDataJSON) 
        print(response)
        # response=response.content.decode("utf-8")
        # print(response)
        # response_JSON=json.loads(response)
        # print(response_JSON)

# Crea un servicio
def crea_servicio(numero_servicio,
                  tipo_servicio,
                  lugar,
                  seguimiento,
                  identificacion_cliente,
                  nombre_cliente,
                  direccion_cliente,
                  modelo,
                  marca, 
                  producto,
                  serie,
                  documento_referencia,
                  falla,
                  accesorios,
                  obervacion
                  ):
        ContextData=open('orion_servicio.json')
       # print(ContextData)
        ContextDataJSON=json.load(ContextData)
        ContextDataJSON['id']=numero_servicio
        ContextDataJSON['type']='servicio'  
        ContextDataJSON['tipo_servicio']['value']=tipo_servicio        
        ContextDataJSON['lugar']['value']=lugar
        ContextDataJSON['seguimiento']['value']=seguimiento 
        ContextDataJSON['identificacion_cliente']['value']=identificacion_cliente 
        ContextDataJSON['direccion_cliente']['value']=direccion_cliente 
        ContextDataJSON['modelo']['value']=modelo 
        ContextDataJSON['marca']['value']=marca 
        ContextDataJSON['producto']['value']=producto 
        ContextDataJSON['serie']['value']=serie 
        ContextDataJSON['documento_referencia']['value']=documento_referencia 
        ContextDataJSON['falla']['value']=falla 
        ContextDataJSON['accesorios']['value']=accesorios 
        ContextDataJSON['obervacion']['value']=obervacion 
        ContextDataJSON['tipo']['value']='servicio' # Para filtrar datos desde fiware orion
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
        headers={"Accept":"application/json"}
        response=requests.post(url,headers=headers,json=ContextDataJSON) 
        print(response)
        # response=response.content.decode("utf-8")
        # print(response)
        # response_JSON=json.loads(response)
        # print(response_JSON)
        
# Crea un usuario
def crea_usuario(nombre,
                  cedula,
                  rol,
                  servicio,
                  nickname,
                  mail,
                  accion,
                  password
                  ):
        ContextData=open('orion_usuario.json')
       # print(ContextData)
        ContextDataJSON=json.load(ContextData)
        ContextDataJSON['id']=str(cedula)
        ContextDataJSON['type']='usuario'  
        ContextDataJSON['nombre']['value']=nombre        
        ContextDataJSON['cedula']['value']=cedula
        ContextDataJSON['rol']['value']=rol 
        ContextDataJSON['servicio']['value']=servicio 
        ContextDataJSON['nickname']['value']=nickname 
        ContextDataJSON['mail']['value']=mail 
        ContextDataJSON['accion']['value']=accion 
        ContextDataJSON['password']['value']=password 
        ContextDataJSON['tipo']['value']='usuario' # Para filtrar datos desde fiware orion
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
        headers={"Accept":"application/json"}
        response=requests.post(url,headers=headers,json=ContextDataJSON) 
        print(response)
        # response=response.content.decode("utf-8")
        # print(response)
        # response_JSON=json.loads(response)
        # print(response_JSON)
  

# Crea un contacto
def crea_contacto(tipo_contacto,
                  tipo_identidad,
                  identidad,
                  nombre,
                  direccion,
                  telefono,
                  departamento,
                  localidad,
                  email
                  ):
        ContextData=open('orion_contacto.json')
       # print(ContextData)
        ContextDataJSON=json.load(ContextData)
        ContextDataJSON['id']=str(identidad)
        ContextDataJSON['type']='contacto'  
        
        ContextDataJSON['tipo_contacto']['value']=tipo_contacto        
        ContextDataJSON['tipo_identidad']['value']=tipo_identidad
        ContextDataJSON['identidad']['value']=identidad 
        ContextDataJSON['nombre']['value']=nombre 
        ContextDataJSON['direccion']['value']=direccion 
        ContextDataJSON['telefono']['value']=telefono 
        ContextDataJSON['departamento']['value']=departamento 
        ContextDataJSON['localidad']['value']=localidad 
        ContextDataJSON['email']['value']=email 
        
        ContextDataJSON['tipo']['value']='contacto' # Para filtrar datos desde fiware orion
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
        headers={"Accept":"application/json"}
        response=requests.post(url,headers=headers,json=ContextDataJSON) 
        print(response)
        # response=response.content.decode("utf-8")
        # print(response)
        # response_JSON=json.loads(response)
        # print(response_JSON)
              
  
#############    
# Para testeo
############# 
# Crea una entidad
def crea_entidad(id_entiti,type_entiti):
        ContextData=open('orion_simple_entiti.json')
       # print(ContextData)
        ContextDataJSON=json.load(ContextData)
        ContextDataJSON['id']=id_entiti
        ContextDataJSON['type']=type_entiti  
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'
        headers={"Accept":"application/json"}
        response=requests.post(url,headers=headers,json=ContextDataJSON) 
        print(response)
        if response.status_code!=422:# print(response.status_code)
            print("Entidad creada")
        if response.status_code==422:# print(response.status_code)
            print("La entidad ya existe")
        
# def crea_sub_entidad(ruta,id_entiti,type_entiti):
#         ContextData=open('simple_entiti.json')
#        # print(ContextData)
#         ContextDataJSON=json.load(ContextData)
#         ContextDataJSON['id']=id_entiti
#         ContextDataJSON['type']=type_entiti  
#         url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities'+ruta
#         headers={"Accept":"application/json"}
#         response=requests.post(url,headers=headers,json=ContextDataJSON) 
#         print(response)
#         if response.status_code!=422:# print(response.status_code)
#             print("Entidad creada")
#         if response.status_code==422:# print(response.status_code)
#             print("La entidad ya existe")

def borra_entidad(id_entiti):
        url='http://'+IP_Orion+':'+Port_Orion+'/v2/entities/'+id_entiti
        headers={"Accept":"application/json"}
        response=requests.delete(url,headers=headers)
        # print(response.status_code)
        # print(response.content
    
# version()
# def crea_cliente(Nombre,Ciudad,Dirección,Cédula,Telefono):
    
# for i in range(10001,20000):
#     crea_cliente("Iván Cúmátóá","Cali","Cll 147 # 7g - 84",str(i),str(i))
#     # time.sleep(0.001)
#     print(i)
# for i in range(20001,30000):
#     crea_cliente("Iván Cúmátóá","Pasto","Cll 147 # 7g - 84",str(i),str(i))
#     # time.sleep(0.001)
#     print(i)

# crea_cliente("Caro","Bogotá","Cll 147 # 7g - 84","fddfdff","3017911256")

# crea_servicio('aargjra5','tipo_servicio','lugar','seguimiento', 'identificacion_cliente','nombre_cliente','direccion_cliente','modelo','marca', 'producto','serie','documento_referencia','falla','accesorios','obervacion')

# crea_usuario('Lennin Escobar',
#             'cc1085254913',
#             'rol',
#             'servicio',
#             'Urcunina',
#             'leescobarm@unal.edu.co',
#             'accion',
#             '123'
#             )

# consulta_entiti('20212334454555')
# crea_contacto("tipo_contacto",
#                   "tipo_identidad",
#                   "1085254913",
#                   "nombre",
#                   "direccion",
#                   "telefono",
#                   "departamento",
#                   "localidad",
#                   "email")                  
# login_get_password('cc1085254913')
# login_get_password('rgrgweh')
# consulta_entiti('5000')
# consulta_entiti_atributo('tipo','servicio')
# consulta_entiti_atributo('Ciudad','Pasto')
# consulta_entiti_atributo('type','Cliente')
# consulta_entiti_atributo('id','5677')
# consulta_entiti('Capital_humano/Tecnicos')
        # consulta_entiti_atributo

## Creamos las entidades
# crea_entidad('Cliente_4','Tecnico')
# crea_entidad('12374754','Orden')

# todas_entidades()


# crea_sub_entidad('Capital_humano','Tecnicos','Humanos')
# todas_entidades()
# time.sleep(1)
# borra_entidad('1085254913')
# borra_entidad('Cliente_1')
# borra_entidad('Cliente_2')



