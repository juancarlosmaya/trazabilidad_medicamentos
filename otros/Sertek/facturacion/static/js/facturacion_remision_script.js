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
  // document.getElementById('form_crear_contacto').reset
};


const modal_edit=document.getElementById('modal_edit');
const openmodal_edit= (a) =>{
  modal_edit.showModal();
};

const closemodal_edit= () =>{
  modal_edit.close();
};






const modal_delete=document.getElementById('modal_edit');
const openmodal_delete= (a) =>{
  document.getElementById('eliminar_remision_message').textContent = '¿Desea eliminar la remisión '+ a.remision.value +'?'
  document.getElementById('numero_remision').textContent = a.remision.value
  document.getElementById('numero_servicio').textContent = a.servicio.value
  modal_delete.showModal(); 
};

const closemodal_delete= () =>{
  modal_delete.close();
};



// Busca contactos

function BuscarContactos(){
  const lista=document.getElementById('tabla_body')
  if (document.getElementById('search_contacto_keep').value !=""){    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/facturacion/busca_remision?search="+document.getElementById('search_contacto_keep').value+'&'+
                                                "activa="+document.getElementById('remision_activa').checked+'&'+
                                                "por_pagina="+document.getElementById('por_pagina').value+'&'+
                                                "actual_page=1" );
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
    xhr.open("GET", "/facturacion/busca_remision?search="+document.getElementById('search_contacto_keep').value+'&'+"por_pagina="+document.getElementById('por_pagina').value+'&'+"actual_page="+document.getElementById('actual_page').value );
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


// Elimina remisión
function elimina_remision(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/elimina_remision?"+"id_remision="+document.getElementById('numero_remision').textContent+'&'+
                                                       "servicio="+document.getElementById('numero_servicio').textContent );
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);  
    closemodal_edit(); 
    BuscarContactos();
  }
  else{
    alert("Error en el servidor web")
  }
  };  
}

function ver_servicio(a){
  window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+a + '&' + "modal_ver_remision_state=true" ;
}






