// Realiza busqueda de servicios
window.onload = (event) => {
  // BuscarServicios();
}



function BusquedaParam(){
    // Realizamos busqueda usando los parámetros
    const lista_servicios_sin_asignar=document.getElementById('tabla_body')
    const xhr = new XMLHttpRequest();
    var e = document.getElementById("lista_tecnicos");
    // var value=e.options[e.selectedIndex].value;// get selected option value
    var text=e.options[e.selectedIndex].text;
    xhr.open("GET", "/pagos/search?"+"estado="+document.getElementById('estado').value+'&'+
                                      "fecha_inicio="+document.getElementById('fecha_inicio').value+'&'+
                                      "fecha_fin="+document.getElementById('fecha_fin').value+'&'+
                                      "activa="+document.getElementById('activa').value+'&'+
                                      "tecnico="+text+'&'+"por_pagina=5"+'&'+"actual_page=1");
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      try{
        if (xhr.response['inner'] != ""){  
          // alert('asd')
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

function BusquedaParam_aux(){ 
  const lista_servicios_sin_asignar=document.getElementById('tabla_body')
   var e = document.getElementById("lista_tecnicos");
  // var value=e.options[e.selectedIndex].value;// get selected option value
    var text=e.options[e.selectedIndex].text;
    const xhr = new XMLHttpRequest();

  xhr.open("GET", "/pagos/search?"+"estado="+document.getElementById('estado').value+'&'+
                                    "fecha_inicio="+document.getElementById('fecha_inicio').value+'&'+
                                    "fecha_fin="+document.getElementById('fecha_fin').value+'&'+
                                    "por_pagina="+document.getElementById('por_pagina_servicios').value+'&'+
                                    "actual_page="+document.getElementById('actual_page_servicios').value+'&'+
                                    "activa="+document.getElementById('activa').value+'&'+
                                    "tecnico="+text);
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
      BusquedaParam_aux();
  }
}

function page_counter_servicios_sub(){
  if (parseInt(document.getElementById('actual_page_servicios').value) > 1){ 
      document.getElementById('actual_page_servicios').value = parseInt(document.getElementById('actual_page_servicios').value) - 1;
      BusquedaParam_aux();
  }
}

function ver_servicio(a){
  // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+a['servicio']['value'];
  // window.open("/crear_servicio/ver_servicio?" +"servicio="+a['servicio']['value'], "_blank");
  window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+a['servicio']['value'];
}

function pagar(a){
  // Cargamos información
  const lista_partes=document.getElementById('tabla_partes')
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/pagos/get_partes?"+"servicio="+a.servicio.value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    lista_partes.innerHTML = xhr.response['partes']; 
  }
  };

  document.getElementById('servicio').textContent=a.servicio.value
  document.getElementById('tecnico').textContent=a.tecnico.value
  document.getElementById('estado_aux').textContent=a.estado.value
  document.getElementById('fecha').textContent=a.fecha_estado.value.split('T')[0]
  document.getElementById('usuario').textContent=a.usuario.value
  document.getElementById('id_estado').textContent=a.id
  // document.getElementById('valor').textContent=a.usuario.value
  openmodal();
  // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+a['servicio']['value'];
  // window.open("/crear_servicio/ver_servicio?" +"servicio="+a['servicio']['value'], "_blank");
}


const modal=document.getElementById('modal');
const openmodal= () =>{
  document.getElementById('boton_pago').setAttribute("onclick", "alerta_boton_pagar()");
  document.getElementById('boton_pago').style.backgroundColor= 'red';
  document.getElementById('valor').textContent= '';
  modal.showModal();
};

const closemodal= () =>{
  document.getElementById('parte_id').textContent=''
  document.getElementById('id_estado').textContent=''
  modal.close();
};

function seleccion_pago(a){
  document.getElementById('parte_id').textContent=a.id
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/pagos/carga_valor?"+"servicio="+a.servicio.value+'&'+
                                        "parte_id="+a.id);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    document.getElementById('valor').textContent= xhr.response['valor'];
    document.getElementById('boton_pago').setAttribute("onclick", "realiza_pago()");
    document.getElementById('boton_pago').style.backgroundColor= 'green';
  }
  };

}

function alerta_boton_pagar(){
  alert('Debe seleccionar la actividad a pagar')
}

function realiza_pago(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/pagos/realiza_pago?"+"id_estado="+document.getElementById('id_estado').textContent+'&'+
                                        "parte_id="+document.getElementById('parte_id').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message'])
    closemodal();
  //   document.getElementById('valor').textContent= xhr.response['valor'];
  //   document.getElementById('boton_pago').setAttribute("onclick", "realiza_pago()");
  //   document.getElementById('boton_pago').style.backgroundColor= 'green';
  }
  };
}
  




















