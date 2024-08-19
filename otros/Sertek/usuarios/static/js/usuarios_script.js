// // Realiza busqueda de servicios
// window.onload = (event) => {
//   BuscarContactos();
// }

const modal=document.getElementById('modal');
const openmodal= () =>{
  modal.showModal();
};
const closemodal= () =>{
  modal.close();
  document.getElementById("form_crear_contacto").reset();
};


const modal_2=document.getElementById('modal_notificacion');
const openmodal_2= () =>{
  modal_2.showModal();
};
const closemodal_2= () =>{
  modal_2.close();
};


const modal_edit=document.getElementById('modal_edit');
const openmodal_edit= (a) =>{
  modal_edit.showModal();
  for (let i = 0; i < document.getElementById('tipo_contacto_edit').children.length; i++) {
    document.getElementById('tipo_contacto_edit').children[i].hidden = false;
  }
  for (let i = 0; i < document.getElementById('tipo_identidad_edit').children.length; i++) {
    document.getElementById('tipo_identidad_edit').children[i].hidden = false;
  }
  for (let i = 0; i < document.getElementById('departamento_edit').children.length; i++) {
    document.getElementById('departamento_edit').children[i].hidden = false;
  }  
  document.getElementById('tipo_contacto_edit').readOnly  = false;
  document.getElementById('tipo_identidad_edit').readOnly  = false;
  document.getElementById('identidad_edit').readOnly  = true;
  document.getElementById('nombre_edit').readOnly  = false;
  document.getElementById('direccion_edit').readOnly  = false;
  document.getElementById('telefono_edit').readOnly  = false;
  document.getElementById('departamento_edit').readOnly  = false;
  document.getElementById('localidad_edit').readOnly  = false;
  document.getElementById('email_edit').readOnly  = false;

  document.getElementById('tipo_contacto_edit').value = a.tipo_contacto.value;
  document.getElementById('tipo_identidad_edit').value = a.tipo_identidad.value;
  document.getElementById('identidad_edit').value = a.identidad.value;
  document.getElementById('nombre_edit').value = a.nombre.value;
  document.getElementById('direccion_edit').value = a.direccion.value;
  document.getElementById('telefono_edit').value = a.telefono.value;
  document.getElementById('departamento_edit').value = a.departamento.value;
  document.getElementById('localidad_edit').value = a.localidad.value;
  document.getElementById('email_edit').value = a.email.value;

  document.getElementById('titulo').textContent = "Editar contacto";
  document.getElementById('accion').textContent = "Guardar";
  document.getElementById('accion').setAttribute('onclick','editar_contacto()')
  document.getElementById('titulo').style.color = "rgb(21, 101, 192)"
  document.getElementById('editar_flag').value = "1";
  document.getElementById('icon_titulo').name = "pencil-outline";
  document.getElementById('icon_titulo').style.color = "rgb(21, 101, 192)"
};

const closemodal_edit= () =>{
  modal_edit.close();
};

const closemodal_delete= () =>{
  modal_edit.close();
};


const modal_delete=document.getElementById('modal_edit');
const openmodal_delete= (a) =>{
  modal_delete.showModal();
  document.getElementById('tipo_contacto_edit').value = a.tipo_contacto.value;
  document.getElementById('tipo_identidad_edit').value = a.tipo_identidad.value;
  document.getElementById('identidad_edit').value = a.identidad.value;
  document.getElementById('nombre_edit').value = a.nombre.value;
  document.getElementById('direccion_edit').value = a.direccion.value;
  document.getElementById('telefono_edit').value = a.telefono.value;
  document.getElementById('departamento_edit').value = a.departamento.value;
  document.getElementById('localidad_edit').value = a.localidad.value;
  document.getElementById('email_edit').value = a.email.value;
  document.getElementById('tipo_contacto_edit').readOnly  = true;
  for (let i = 0; i < document.getElementById('tipo_contacto_edit').children.length; i++) {
    document.getElementById('tipo_contacto_edit').children[i].hidden = true;
  }
  document.getElementById('tipo_identidad_edit').readOnly  = true;
  for (let i = 0; i < document.getElementById('tipo_identidad_edit').children.length; i++) {
    document.getElementById('tipo_identidad_edit').children[i].hidden = true;
  }
  document.getElementById('identidad_edit').readOnly  = true;
  document.getElementById('nombre_edit').readOnly  = true;
  document.getElementById('direccion_edit').readOnly  = true;
  document.getElementById('telefono_edit').readOnly  = true;
  document.getElementById('departamento_edit').readOnly  = true;
  for (let i = 0; i < document.getElementById('departamento_edit').children.length; i++) {
    document.getElementById('departamento_edit').children[i].hidden = true;
  }
  document.getElementById('localidad_edit').readOnly  = true;
  document.getElementById('email_edit').readOnly  = true;

  
  document.getElementById('titulo').textContent = "Eliminar contacto";
  document.getElementById('titulo').style.color = "red";
  document.getElementById('accion').textContent = "Eliminar";
  document.getElementById('accion').style.color = "red";
  document.getElementById('accion').setAttribute('onclick','eliminar_contacto()')
  document.getElementById('editar_flag').value = "2";
  document.getElementById('icon_titulo').name = "trash-outline";
  document.getElementById('icon_titulo').style.color = "red"
  
};

function editar_contacto(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/cliente_proveedor/editar_contacto?"+"tipo_contacto="+document.getElementById('tipo_contacto_edit').value+'&'+
                                                        "tipo_identidad="+document.getElementById('tipo_identidad_edit').value+'&'+
                                                        "identidad="+document.getElementById('identidad_edit').value+'&'+
                                                        "nombre="+document.getElementById('nombre_edit').value+'&'+
                                                        "direccion="+encodeURIComponent(document.getElementById('direccion_edit').value)+'&'+
                                                        "telefono="+encodeURIComponent(document.getElementById('telefono_edit').value)+'&'+
                                                        "departamento="+document.getElementById('departamento_edit').value+'&'+
                                                        "localidad="+document.getElementById('localidad_edit').value+'&'+
                                                        "email="+encodeURIComponent(document.getElementById('email_edit').value));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message'])   
    closemodal_edit();
    BuscarContactos_aux(); 
  }
  else{
    alert("Error en el servidor web")
  }
  };
}


// Crear contacto tras submit en el modal
let loginForm = document.getElementById("form_crear_contacto");
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/cliente_proveedor/crear_contacto?"+"tipo_contacto="+document.getElementById('tipo_contacto').value+'&'+
                                                          "tipo_identidad="+document.getElementById('tipo_identidad').value+'&'+
                                                          "identidad="+document.getElementById('identidad').value+'&'+
                                                          "nombre="+document.getElementById('nombre').value+'&'+
                                                          "direccion="+encodeURIComponent(document.getElementById('direccion').value)+'&'+
                                                          "telefono="+encodeURIComponent(document.getElementById('telefono').value)+'&'+
                                                          "departamento="+document.getElementById('departamento').value+'&'+
                                                          "localidad="+document.getElementById('localidad').value+'&'+
                                                          "email="+encodeURIComponent(document.getElementById('email').value));
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


// Busca contactos

function BuscarContactos(){
  const lista=document.getElementById('tabla_body')
  if (document.getElementById('search_contacto_keep').value !=""){    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cliente_proveedor/busca_contactos?search="+document.getElementById('search_contacto_keep').value+'&'+"por_pagina="+document.getElementById('por_pagina').value+'&'+"actual_page=1" );
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista.innerHTML = options_inner; 
          document.getElementById('num_pages').value= xhr.response['num_pages']
          document.getElementById('actual_page').value = 1;
          // document.getElementById('por_pagina').value = 5
          document.getElementById('total_items').textContent  = document.getElementById('actual_page').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista.innerHTML = options_inner; 
          document.getElementById('num_pages').value= 0
          document.getElementById('actual_page').value = 1;
          document.getElementById('por_pagina').value = 5
          document.getElementById('total_items').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista.innerHTML = options_inner; 
        document.getElementById('num_pages').value= 0
        document.getElementById('actual_page').value = 1;
        document.getElementById('por_pagina').value = 5
        document.getElementById('total_items').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{    
      options_inner=null;
      lista.innerHTML = options_inner; 
      document.getElementById('num_pages').value= 0
      document.getElementById('actual_page').value = 1;
      document.getElementById('total_items').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    }; 
} 
else{
    options_inner=null;
    lista.innerHTML = options_inner; 
    document.getElementById('num_pages').value= 0
    document.getElementById('actual_page').value = 1;
    document.getElementById('por_pagina').value = 5
    document.getElementById('total_items').textContent  = "0 de 0";
}  
}

var input = document.getElementById("search_contacto");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    document.getElementById('search_contacto_keep').value = document.getElementById('search_contacto').value 
    BuscarContactos();
  }
}); 

var boton_search = document.getElementById("boton_search");
boton_search.addEventListener("click", function(event) {
    document.getElementById('search_contacto_keep').value = document.getElementById('search_contacto').value 
    BuscarContactos();
});

function BuscarContactos_aux(){ 
  const lista=document.getElementById('tabla_body')
  if (document.getElementById('search_contacto_keep').value != ""){    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cliente_proveedor/busca_contactos?search="+document.getElementById('search_contacto_keep').value+'&'+"por_pagina="+document.getElementById('por_pagina').value+'&'+"actual_page="+document.getElementById('actual_page').value );
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          options_inner=xhr.response['inner'];
          lista.innerHTML = options_inner;
          document.getElementById('actual_page').value =xhr.response['actual_page']; 
          document.getElementById('num_pages').value= xhr.response['num_pages'];
          document.getElementById('total_items').textContent  = document.getElementById('actual_page').value + ' de '+  xhr.response['num_pages'];
        }
        if (xhr.response['inner'] == ""){
          options_inner=null;
          lista.innerHTML = options_inner; 
          document.getElementById('num_pages').value= 0;
          document.getElementById('actual_page').value = 1;
          document.getElementById('total_items').textContent  = "0 de 0";
        }
      }
      catch{
        options_inner=null;
        lista.innerHTML = options_inner; 
        document.getElementById('num_pages').value= 0;
        document.getElementById('actual_page').value = 1;
        document.getElementById('total_items').textContent  = "0 de 0";
        alert("Error en la base de datos, requiere servicio técnico.")
      }   
    }
    else{
      options_inner=null;
      lista.innerHTML = options_inner; 
      document.getElementById('num_pages').value= 0;
      document.getElementById('actual_page').value = 1;
      document.getElementById('total_items').textContent  = "0 de 0";
      alert("Error en el servidor web")
    }
    };
  }    
}

function page_counter_add(){
  if (parseInt(document.getElementById('actual_page').value) < parseInt(document.getElementById('num_pages').value)){ 
      document.getElementById('actual_page').value = parseInt(document.getElementById('actual_page').value) + 1;
      BuscarContactos_aux();
  }
}

function page_counter_sub(){
  if (parseInt(document.getElementById('actual_page').value) > 1){ 
      document.getElementById('actual_page').value = parseInt(document.getElementById('actual_page').value) - 1;
      BuscarContactos_aux();
  }
}


function eliminar_contacto(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/cliente_proveedor/eliminar_contacto?"+"entity="+document.getElementById('identidad_edit').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message'])   
    closemodal_edit();
    BuscarContactos_aux(); 
  }
  else{
    alert("Error en el servidor web")
  }
  };
}






