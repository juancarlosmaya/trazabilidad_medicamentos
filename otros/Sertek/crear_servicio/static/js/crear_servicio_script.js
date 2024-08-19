// Realiza busqueda de servicios
window.onload = (event) => {
  BuscarServicios();
}

function BuscarServicios(){
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/buscar_servicios_filtro?"+"search="+document.getElementById('search').value+'&'+
                                                               "asigna="+document.getElementById('asigna').value+'&'+
                                                               "atributo="+document.getElementById('atributo').value+'&'+
                                                               "por_pagina=5"+'&'+"actual_page=1");
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista_servicios_sin_asignar.innerHTML = options_inner; 
          document.getElementById('num_pages_servicios').value= xhr.response['num_pages']
          document.getElementById('actual_page_servicios').value = 1;
          document.getElementById('por_pagina_servicios').value = 5
          document.getElementById('total_items_servicios_sin_asignar').textContent  = document.getElementById('actual_page').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista_servicios_sin_asignar.innerHTML = options_inner; 
          document.getElementById('num_pages_servicios').value= 0
          document.getElementById('actual_page_servicios').value = 1;
          document.getElementById('por_pagina_servicios').value = 5
          document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista_servicios_sin_asignar.innerHTML = options_inner; 
        document.getElementById('num_pages_servicios').value= 0
        document.getElementById('actual_page_servicios').value = 1;
        document.getElementById('por_pagina_servicios').value = 5
        document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{    
      options_inner=null;
      lista_servicios_sin_asignar.innerHTML = options_inner; 
      document.getElementById('num_pages_servicios').value= 0
      document.getElementById('actual_page_servicios').value = 1;
      document.getElementById('por_pagina_servicios').value = 5
      document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    }; 
}   

function BuscarServicios_aux(){ 
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/buscar_servicios_filtro?"+"por_pagina="+document.getElementById('por_pagina_servicios').value+'&'+
                                                               "actual_page="+document.getElementById('actual_page_servicios').value+'&'+
                                                               "search="+document.getElementById('search').value+'&'+
                                                               "asigna="+document.getElementById('asigna').value+'&'+
                                                               "atributo="+document.getElementById('atributo').value+'&');
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista_servicios_sin_asignar.innerHTML = options_inner; 
          document.getElementById('num_pages_servicios').value= xhr.response['num_pages']
          document.getElementById('actual_page_servicios').value = xhr.response['actual_page'];
          // document.getElementById('por_pagina_servicios').value = xhr.response['num_pages']
          document.getElementById('total_items_servicios_sin_asignar').textContent  = document.getElementById('actual_page_servicios').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista_servicios_sin_asignar.innerHTML = options_inner; 
          document.getElementById('num_pages_servicios').value= 0
          document.getElementById('actual_page_servicios').value = 1;
          document.getElementById('por_pagina_servicios').value = 5
          document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista_servicios_sin_asignar.innerHTML = options_inner; 
        document.getElementById('num_pages_servicios').value= 0
        document.getElementById('actual_page_servicios').value = 1;
        document.getElementById('por_pagina_servicios').value = 5
        document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{    
      options_inner=null;
      lista_servicios_sin_asignar.innerHTML = options_inner; 
      document.getElementById('num_pages_servicios').value= 0
      document.getElementById('actual_page_servicios').value = 1;
      document.getElementById('por_pagina_servicios').value = 5
      document.getElementById('total_items_servicios_sin_asignar').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    }; 
}






function page_counter_servicios_add(){
  if (parseInt(document.getElementById('actual_page_servicios').value) < parseInt(document.getElementById('num_pages_servicios').value)){ 
      document.getElementById('actual_page_servicios').value = parseInt(document.getElementById('actual_page_servicios').value) + 1;
      BuscarServicios_aux();
  }
}

function page_counter_servicios_sub(){
  if (parseInt(document.getElementById('actual_page_servicios').value) > 1){ 
      document.getElementById('actual_page_servicios').value = parseInt(document.getElementById('actual_page_servicios').value) - 1;
      BuscarServicios_aux();
  }
}


const modal_asignar_tecnico=document.getElementById('modal_asignar_tecnico');
const openmodal_asignar_tecnico= (a) =>{
  modal_asignar_tecnico.showModal();
  document.getElementById('numero_servicio').value = a['id'];
  lista_tecnicos();
};

const closemodal_asignar_tecnico= () =>{
  modal_asignar_tecnico.close();
};

const modal=document.getElementById('modal');
const openmodal= () =>{
  modal.showModal();
};

const closemodal= () =>{
  modal.close();
  document.getElementById("form_crear").reset();
};


const modal_2=document.getElementById('modal_notificacion');
const openmodal_2= () =>{
  modal_2.showModal();
};

const closemodal_2= () =>{
  modal_2.close();
};

const modal_crear_cliente=document.getElementById('modal_crear_cliente');
const openmodal_crear_cliente= (a) =>{
  modal_crear_cliente.showModal();
  
};

const closemodal_crear_cliente= () =>{
  modal_crear_cliente.close();
  document.getElementById("form_crea_cliente").reset();
};

const modal_busqueda=document.getElementById('modal_busqueda');
const openmodal_busqueda= () =>{
  modal_busqueda.showModal();
};

const closemodal_busqueda= () =>{
  const borra_lista=document.getElementById('resultados_body')
  modal_busqueda.close();
  borra_lista.innerHTML = ''; 
  document.getElementById('search_cliente').value= '';
  document.getElementById('num_pages').value= 0
  document.getElementById('actual_page').value = 1;
  document.getElementById('por_pagina').value = 5
  document.getElementById('total_items_cliente').textContent  = "0 de 0";
  
};

const asignar_cliente= (z) =>{
  document.getElementById('nombre').value = z.nombre.value;
  document.getElementById('direccion').value = z.direccion.value;
  document.getElementById('identidad').value = z.identidad.value;

  document.getElementById('email').value = z.email.value;
  document.getElementById('localidad').value = z.localidad.value;
  document.getElementById('telefono').value = z.telefono.value;
  closemodal_busqueda();
};

const modal_crear_modelo=document.getElementById('modal_crear_modelo');
const openmodal_crear_modelo= () =>{
  modal_crear_modelo.showModal();
  
};

const closemodal_crear_modelo= () =>{
  modal_crear_modelo.close();
  document.getElementById("form_crea_modelo").reset();
};

function BuscaCliente(){ 
  if (document.getElementById('identidad').value !=""){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/search_cliente?search="+document.getElementById('identidad').value);
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      if (xhr.response != null){   
        try{
          document.getElementById('identidad').value = xhr.response['id'];
          document.getElementById('nombre').value = xhr.response['nombre']['value'];
          document.getElementById('direccion').value = xhr.response['direccion']['value'];
        } 
        catch{
          document.getElementById('identidad').value = null;
          document.getElementById('nombre').value = null;
          document.getElementById('direccion').value = null;
          alert("El cliente no existe")         
        }          
        }
      if (xhr.response == null){    
          document.getElementById('identidad').value = null;
          document.getElementById('nombre').value = null;
          document.getElementById('direccion').value = null;
          alert("Error en la base de datos")
        }     
    }
    else{
      alert("Error en el servidor web")
    }
    }; 
  } 
  else{
    document.getElementById('identidad').value = null;
    document.getElementById('nombre').value = null;
    document.getElementById('direccion').value = null;
  }  
}

function BuscarClientes(){
  const lista_clientes=document.getElementById('resultados_body')
  if (document.getElementById('search_cliente_keep').value !=""){    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/buscar_clientes?search_clientes="+document.getElementById('search_cliente_keep').value+'&'+"por_pagina="+document.getElementById('por_pagina').value+'&'+"actual_page=1" );
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista_clientes.innerHTML = options_inner; 
          document.getElementById('num_pages').value= xhr.response['num_pages']
          document.getElementById('actual_page').value = 1;
          // document.getElementById('por_pagina').value = 5
          document.getElementById('total_items_cliente').textContent  = document.getElementById('actual_page').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista_clientes.innerHTML = options_inner; 
          document.getElementById('num_pages').value= 0
          document.getElementById('actual_page').value = 1;
          document.getElementById('por_pagina').value = 5
          document.getElementById('total_items_cliente').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista_clientes.innerHTML = options_inner; 
        document.getElementById('num_pages').value= 0
        document.getElementById('actual_page').value = 1;
        document.getElementById('por_pagina').value = 5
        document.getElementById('total_items_cliente').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{    
      options_inner=null;
      lista_clientes.innerHTML = options_inner; 
      document.getElementById('num_pages').value= 0
      document.getElementById('actual_page').value = 1;
      document.getElementById('total_items_cliente').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    }; 
} 
else{
    options_inner=null;
    lista_clientes.innerHTML = options_inner; 
    document.getElementById('num_pages').value= 0
    document.getElementById('actual_page').value = 1;
    document.getElementById('por_pagina').value = 5
    document.getElementById('total_items_cliente').textContent  = "0 de 0";
}  
}

var input = document.getElementById("search_cliente");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    document.getElementById('search_cliente_keep').value = document.getElementById('search_cliente').value 
    BuscarClientes();
    // alert("asd")
  }
}); 

var boton_search = document.getElementById("boton_busqueda");
boton_search.addEventListener("click", function(event) {
    document.getElementById('search_cliente_keep').value = document.getElementById('search_cliente').value 
    BuscarClientes();
});


function BuscarClientes_aux(){ 
  const lista_clientes=document.getElementById('resultados_body')
  if (document.getElementById('search_cliente_keep').value != ""){    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/buscar_clientes?search_clientes="+document.getElementById('search_cliente_keep').value+'&'+"por_pagina="+document.getElementById('por_pagina').value+'&'+"actual_page="+document.getElementById('actual_page').value );
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista_clientes.innerHTML = options_inner;
          document.getElementById('actual_page').value =xhr.response['actual_page']; 
          document.getElementById('num_pages').value= xhr.response['num_pages'];
          document.getElementById('total_items_cliente').textContent  = document.getElementById('actual_page').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista_clientes.innerHTML = options_inner; 
          document.getElementById('num_pages').value= 0;
          document.getElementById('actual_page').value = 1;
          document.getElementById('total_items_cliente').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista_clientes.innerHTML = options_inner; 
        document.getElementById('num_pages').value= 0;
        document.getElementById('actual_page').value = 1;
        document.getElementById('total_items_cliente').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{
      options_inner=null;
      lista_clientes.innerHTML = options_inner; 
      document.getElementById('num_pages').value= 0;
      document.getElementById('actual_page').value = 1;
      document.getElementById('total_items_cliente').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    };
  }    
}

function page_counter_add(){
  if (parseInt(document.getElementById('actual_page').value) < parseInt(document.getElementById('num_pages').value)){ 
      document.getElementById('actual_page').value = parseInt(document.getElementById('actual_page').value) + 1;
      BuscarClientes_aux();
  }
}

function page_counter_sub(){
  if (parseInt(document.getElementById('actual_page').value) > 1){ 
      document.getElementById('actual_page').value = parseInt(document.getElementById('actual_page').value) - 1;
      BuscarClientes_aux();
  }
}

function UpdateModels(){ 
  // if (document.getElementById('modelo').value !=""){ 
    const lista_modelos=document.getElementById('lista_modelos')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/lista_modelos");
    xhr.send();
    xhr.responseType = "json";  
    xhr.onload = () => {
    options_inner=xhr.response;
    lista_modelos.innerHTML = options_inner; 
    };
  // }    
}

function BuscaModelo(){
  if (document.getElementById('modelo').value !=""){ 
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/search_modelo?search="+document.getElementById('modelo').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    if (xhr.response != null){   
      try{
        document.getElementById('modelo').value = xhr.response['id'];
        document.getElementById('marca').value = xhr.response['marca']['value'];
        document.getElementById('producto').value = xhr.response['producto']['value'];
      } 
      catch{
        document.getElementById('modelo').value = null;
        document.getElementById('marca').value = null;
        document.getElementById('producto').value = null;
        alert("El modelo no existe")         
      }          
      }
    if (xhr.response == null){    
        document.getElementById('modelo').value = null;
        document.getElementById('marca').value = null;
        document.getElementById('producto').value = null;
        alert("Error en la base de datos")
      }     
  }
  else{
    alert("Error en el servidor web")
  }
  };
  }
  else{
    document.getElementById('modelo').value = null;
    document.getElementById('marca').value = null;
    document.getElementById('producto').value = null;
  }    
}


function CreaCliente(){ 
  const xhr = new XMLHttpRequest();
  xhr.open("GET","/crear_servicio/crear_cliente?"+"tipo_contacto="+document.getElementById('tipo_contacto_crear_cliente').value+'&'+
                                                  "tipo_identidad="+document.getElementById('tipo_identidad_crear_cliente').value+'&'+
                                                  "identidad="+document.getElementById('identidad_crear_cliente').value+'&'+
                                                  "nombre="+document.getElementById('nombre_crear_cliente').value+'&'+
                                                  "direccion="+encodeURIComponent(document.getElementById('direccion_crear_cliente').value)+'&'+   // Campo especial codificado URL
                                                  "telefono="+document.getElementById('telefono_crear_cliente').value+'&'+
                                                  "departamento="+document.getElementById('departamento_crear_cliente').value+'&'+
                                                  "localidad="+document.getElementById('localidad_crear_cliente').value+'&'+
                                                  "email="+encodeURIComponent(document.getElementById('email_crear_cliente').value));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response)    
  }
  else{
    alert("Error en el servidor web")
  }
  };    
}

function CreaModelo(){ 
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/crear_modelo?"+"marca="+document.getElementById('crear_modelo_marca').value+'&'+
                                                  "producto="+document.getElementById('crear_modelo_producto').value+'&'+
                                                  "nombre_producto="+document.getElementById('crear_modelo_nombre').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response)    
  }
  else{
    alert("Error en el servidor web")
  }
  };    
}

// Crear servicio tras submit
let loginForm = document.getElementById("form_crear");
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/crear_nuevo_servicio?"+"tipo_servicio="+document.getElementById('tipo_servicio').value+'&'+
                                                          "lugar="+document.getElementById('lugar').value+'&'+
                                                          "seguimiento="+document.getElementById('seguimiento').value+'&'+
                                                          "sede="+encodeURIComponent(document.getElementById('sede').value)+'&'+
                                                          "identidad="+document.getElementById('identidad').value+'&'+
                                                          "nombre="+document.getElementById('nombre').value+'&'+
                                                          "direccion="+encodeURIComponent(document.getElementById('direccion').value)+'&'+

                                                          "email="+encodeURIComponent(document.getElementById('email').value)+'&'+
                                                          "localidad="+encodeURIComponent(document.getElementById('localidad').value)+'&'+
                                                          "telefono="+encodeURIComponent(document.getElementById('telefono').value)+'&'+

                                                          "modelo="+encodeURIComponent(document.getElementById('modelo').value)+'&'+
                                                          "marca="+document.getElementById('marca').value+'&'+
                                                          "producto="+document.getElementById('producto').value+'&'+
                                                          "serie="+encodeURIComponent(document.getElementById('serie').value)+'&'+
                                                          "doc_ref="+encodeURIComponent(document.getElementById('doc_ref').value)+'&'+
                                                          "falla="+encodeURIComponent(document.getElementById('falla').value)+'&'+
                                                          "accesorios="+encodeURIComponent(document.getElementById('accesorios').value)+'&'+
                                                          "observacion="+encodeURIComponent(document.getElementById('observacion').value));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']) 
    closemodal();   
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});


function lista_tecnicos(){
  const lista_tecnicos=document.getElementById('lista_tecnicos');
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/lista_tecnicos");
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    options_inner= xhr.response['inner'];
    lista_tecnicos.innerHTML = options_inner;    
  }
  else{
    alert("Error en el servidor web")
  }
  };   
}

// Asigna técnico tras submit
let AsignaTecnicoForm = document.getElementById("form_asigna_tecnico");
AsignaTecnicoForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/asigna_tecnico?"+"entity="+document.getElementById('numero_servicio').value+'&'+
                                                    "user="+document.getElementById('lista_tecnicos').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    closemodal_asignar_tecnico();
    BuscarServicios();  
    alert(xhr.response['message']);   
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});

function ver_servicio(a){
  window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+a['id'];
}

// Busqueda con parámetros (filtro) de la página principal
function busqueda_filtro(){
  BuscarServicios(); 
}

// Agrega notas al presionar enter en el campo input
var busqueda = document.getElementById("search");
  busqueda.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      BuscarServicios(); 
    }
    });





















