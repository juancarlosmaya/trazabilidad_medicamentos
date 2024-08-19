// Realiza busqueda de servicios
window.onload = (event) => {
  BuscarServicios();
}

function BuscarServicios(){
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/dashboard/buscar_servicios_filtro?"+"search="+document.getElementById('search').value+'&'+
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

function BuscarServicios_aux(){ 
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/dashboard/buscar_servicios_filtro?"+"por_pagina="+document.getElementById('por_pagina_servicios').value+'&'+
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
      // alert('asdasd')
      BuscarServicios(); 
    }
    });