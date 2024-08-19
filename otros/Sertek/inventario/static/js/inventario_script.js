// Realiza busqueda de servicios
window.onload = (event) => {
  BuscarItems();
}



function BuscarItems(){
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/inventario/buscar_items_filtro?"+"search="+document.getElementById('search').value+'&'+
                                                               "activo="+document.getElementById('activo').value+'&'+
                                                               "atributo="+document.getElementById('atributo').value+'&'+
                                                               "por_pagina=5"+'&'+"actual_page=1");
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    // alert(xhr.response['inner'])
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista_servicios_sin_asignar.innerHTML = options_inner; 
          document.getElementById('num_pages_servicios').value= xhr.response['num_pages']
          document.getElementById('actual_page_servicios').value = 1;
          document.getElementById('por_pagina_servicios').value = 5
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

function BuscarItems_aux(){ 
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/inventario/buscar_items_filtro?"+"por_pagina="+document.getElementById('por_pagina_servicios').value+'&'+
                                                               "actual_page="+document.getElementById('actual_page_servicios').value+'&'+
                                                               "search="+document.getElementById('search').value+'&'+
                                                               "activo="+document.getElementById('activo').value+'&'+
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
      BuscarItems_aux();
  }
}

function page_counter_servicios_sub(){
  if (parseInt(document.getElementById('actual_page_servicios').value) > 1){ 
      document.getElementById('actual_page_servicios').value = parseInt(document.getElementById('actual_page_servicios').value) - 1;
      // alert
      BuscarItems_aux();
  }
}



const modal_crear_item=document.getElementById('modal_crear_item');
const = (a) =>{
  modal_crear_item.showModal();
  
};
const closemodal_crear_item= () =>{
  modal_crear_item.close();
  // document.getElementById("form_crea_cliente").reset();
};

const modal_editar_item=document.getElementById('modal_editar_item');
const openmodal_editar_item= (a) =>{
  modal_editar_item.showModal();
  
};
const closemodal_editar_item= () =>{
  modal_editar_item.close();
  // document.getElementById("form_crea_cliente").reset();
};


const modal_elimina_item=document.getElementById('modal_elimina_item');
const openmodal_elimina_item= (a) =>{
  modal_elimina_item.showModal();
  
};

const closemodal_elimina_item= () =>{
  modal_elimina_item.close();
  // document.getElementById("form_crea_cliente").reset();
};






function CreaItem(){ 
  const xhr = new XMLHttpRequest();
  xhr.open("GET","/inventario/crear_item?"+"referencia="+encodeURIComponent(document.getElementById('referencia').value)+'&'+
                                           "nombre_parte="+encodeURIComponent(document.getElementById('nombre_parte').value)+'&'+
                                           "cantidad="+document.getElementById('cantidad').value+'&'+
                                           "marca="+encodeURIComponent(document.getElementById('marca').value)+'&'+
                                           "precio="+document.getElementById('precio').value+'&'+
                                           "observacion="+encodeURIComponent(document.getElementById('observacion').value)+'&'+   // Campo especial codificado URL
                                           "ciudad="+encodeURIComponent(document.getElementById('ciudad').value));
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


// Busqueda con parámetros (filtro) de la página principal
function busqueda_filtro(){
  BuscarItems(); 
}



function eliminar_item(a){
  document.getElementById('eliminar_item_message').textContent = '¿Desea eliminar el item '+ a.nombre_parte.value+'?'
  // alert(a.id)
  document.getElementById('id_item').textContent = a.id
  openmodal_elimina_item();
}


// Inactiva item
function inactiva_item(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/inventario/elimina_item?"+"item_id="+document.getElementById('id_item').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);   
    closemodal_elimina_item(); 
    BuscarItems_aux();
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio_edit').value; 
    // document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
    // closemodal_modal_elimina_abono();
  }
  else{
    alert("Error en el servidor web")
  }
  };  
}

// Al presionar enter
var busqueda = document.getElementById("search");
  busqueda.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      BuscarItems(); 
    }
    });

function editar_item(a){
  // alert(a.id)
  document.getElementById('id_item_editar').textContent = a.id
  document.getElementById('referencia_editar').value = a.referencia.value
  document.getElementById('nombre_parte_editar').value = a.nombre_parte.value
  document.getElementById('cantidad_editar').value = a.cantidad.value
  document.getElementById('marca_editar').value = a.marca.value
  document.getElementById('precio_editar').value = a.precio.value
  document.getElementById('observacion_editar').value = a.observacion.value
  document.getElementById('ciudad_editar').value = a.ciudad.value
  openmodal_editar_item();

}

function EditarItem(){ 
  const xhr = new XMLHttpRequest();
  xhr.open("GET","/inventario/editar_item?"+"id_item="+encodeURIComponent(document.getElementById('id_item_editar').textContent)+'&'+
                                           "referencia="+encodeURIComponent(document.getElementById('referencia_editar').value)+'&'+
                                           "nombre_parte="+encodeURIComponent(document.getElementById('nombre_parte_editar').value)+'&'+
                                           "cantidad="+document.getElementById('cantidad_editar').value+'&'+
                                           "marca="+encodeURIComponent(document.getElementById('marca_editar').value)+'&'+
                                           "precio="+document.getElementById('precio_editar').value+'&'+
                                           "observacion="+encodeURIComponent(document.getElementById('observacion_editar').value)+'&'+   // Campo especial codificado URL
                                           "ciudad="+encodeURIComponent(document.getElementById('ciudad_editar').value));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message'])  
    BuscarItems_aux();  
    closemodal_editar_item(); 
  }
  else{
    alert("Error en el servidor web")
  }
  };    
}























