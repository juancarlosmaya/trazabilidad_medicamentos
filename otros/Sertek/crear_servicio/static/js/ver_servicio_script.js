const modal_asignar_tecnico=document.getElementById('modal_asignar_tecnico');
const openmodal_asignar_tecnico= (a) =>{
  modal_asignar_tecnico.showModal();
  document.getElementById('numero_servicio').value = a;
  lista_tecnicos();
};

const closemodal_asignar_tecnico= () =>{
  modal_asignar_tecnico.close();
};

//  Asignar estado
const modal_asignar_estado=document.getElementById('modal_asignar_estado');
const openmodal_asignar_estado= (a) =>{
  modal_asignar_estado.showModal();
  document.getElementById('numero_servicio').value = a;
  // lista_tecnicos();
};

const closemodal_asignar_estado= () =>{
  modal_asignar_estado.close();
};


// Modal solicitud de parte
const modal_solicitud=document.getElementById('modal_solicitud');
const openmodal_modal_solicitud= (a) =>{
  document.getElementById('num_servicio').value = a;
  modal_solicitud.showModal();
};

const closemodal_modal_solicitud= () =>{
  modal_solicitud.close();
  document.getElementById('buscar_parte').value=null;
  document.getElementById('nombre_parte').textContent=null;
  document.getElementById('referencia').textContent=null;
  document.getElementById('precio_parte').value=null;
  document.getElementById('cantidad').value = null
  document.getElementById('id_parte').value=null;   
  document.getElementById('tabla_parte').innerHTML = ''; 
};

// Modal elimina solicitud de parte
const modal_elimina_solicitud_parte=document.getElementById('modal_elimina_solicitud_parte');
const openmodal_modal_elimina_solicitud_parte= () =>{
  // document.getElementById('num_servicio').value = a;
  modal_elimina_solicitud_parte.showModal();
};

const closemodal_modal_elimina_solicitud_parte= () =>{
  modal_elimina_solicitud_parte.close();
};

// Modal elimina estad0
const modal_elimina_estado=document.getElementById('modal_elimina_estado');
const openmodal_modal_elimina_estado= () =>{
  // document.getElementById('num_servicio').value = a;
  modal_elimina_estado.showModal();
};

const closemodal_modal_elimina_estado= () =>{
  modal_elimina_estado.close();
};

// Modal crea remisión
const modal_remision=document.getElementById('modal_remision');
const openmodal_modal_remision= () =>{
  document.getElementById("forma_remision").reset();
  modal_remision.showModal();
};

const closemodal_modal_remision= () =>{
  // Resetear los campos forma_remision
  document.getElementById("forma_remision").reset();
  
  modal_remision.close();
};

// Modal ver remisión
const modal_ver_remision=document.getElementById('modal_ver_remision');
const openmodal_modal_ver_remision= () =>{
  modal_ver_remision.showModal();
};

const closemodal_modal_ver_remision= () =>{
  modal_ver_remision.close();
};

// Modal abono
const modal_abono=document.getElementById('modal_abono');
const openmodal_modal_abono= () =>{
  modal_abono.showModal();

};

const closemodal_modal_abono= () =>{
  modal_abono.close();
  document.getElementById('detalle').value=null;
  document.getElementById('valor_abono').value=null;
  document.getElementById('medio_de_pago').value="";
  // document.getElementById('precio_parte').value=null;
  // document.getElementById('cantidad').value = null  
};

// Modal elimina abono de parte
const modal_elimina_abono=document.getElementById('modal_elimina_abono');
const openmodal_modal_elimina_abono= () =>{
  modal_elimina_abono.showModal();
};
const closemodal_modal_elimina_abono= () =>{
  modal_elimina_abono.close();
};


// Modal abonos detalle
const modal_abono_datalle=document.getElementById('modal_abonos_detalle');
const openmodal_abono_datalle= () =>{
  modal_abono_datalle.showModal();
};

const closemodal_abono_datalle= () =>{
  modal_abono_datalle.close();
};

// gggggg
function lista_tecnicos(){
  const lista_tecnicos=document.getElementById('lista_tecnicos');
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/lista_tecnicos_lugar?servicio="+document.getElementById('numero_servicio').value);
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
let AsignaTecnicoForm = document.getElementById("form_asigna_tecnicos");
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
    alert(xhr.response['message']); 
    if ("El técnico fue asignado"==xhr.response['message']){
      document.getElementById('tecnico').textContent = document.getElementById('lista_tecnicos').options[document.getElementById('lista_tecnicos').selectedIndex].text;
    } 
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});

// Crea abono tras submit
let CreaAbonoForm = document.getElementById("form_abono");
CreaAbonoForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/crea_abono?"+"servicio="+document.getElementById('servicio').textContent+'&'+
                                                "medio_de_pago="+document.getElementById('medio_de_pago').value+'&'+
                                                "nombre_razon_social="+document.getElementById('nombre_razon_social').textContent+'&'+
                                                "detalle="+document.getElementById('detalle').value+'&'+
                                                "valor_abono="+document.getElementById('valor_abono').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']); 
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio').textContent;
    document.getElementById('total_abonos').textContent = xhr.response['total_abonos']; 
    // Actualiza total abonos de la remision
    document.getElementById('total_abonos_remision').textContent = xhr.response['total_abonos'];
    update_mensajes();
    closemodal_modal_abono();
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});

// Agrega notas al presionar enter en el campo input
var input = document.getElementById("input_nota");
var div_mensajes = document.getElementById("div_mensajes");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/crea_mensaje?"+"servicio="+document.getElementById('servicio').textContent+'&'+
                                                  "mensaje="+document.getElementById('input_nota').value);
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      document.getElementById('input_nota').value='';;
      div_mensajes.innerHTML = xhr.response['mensajes_html']; 
      document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight  
    }
    else{
      alert("Error en el servidor web")
    }
    };
  }
}); 

// Agrega notas al presionar el boton
var div_mensajes = document.getElementById("div_mensajes");
document.getElementById('boton_nota').addEventListener("click", function() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/crea_mensaje?"+"servicio="+document.getElementById('servicio').textContent+'&'+
                                                  "mensaje="+document.getElementById('input_nota').value);
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      document.getElementById('input_nota').value='';;
      div_mensajes.innerHTML = xhr.response['mensajes_html']; 
      document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight  
    }
    else{
      alert("Error en el servidor web")
    }
    };
}); 


// Abonos detalles
function abonos_detalle(){
  
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/lista_detalle_abonos?"+"servicio="+document.getElementById('servicio').textContent);
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      // alert(xhr.response['message']); 
      // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio').textContent;
      // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio').textContent;
      document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
      openmodal_abono_datalle();
    }
    else{
      alert("Error en el servidor web")
    }
    };
}

// Busca las partes al presionar enter en el campo buscar partes
var buscar_parte = document.getElementById("buscar_parte");
var tabla_parte = document.getElementById("tabla_parte");
buscar_parte.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/lista_partes?"+"parte="+document.getElementById('buscar_parte').value)
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      // document.getElementById('input_nota').value='';;
      tabla_parte.innerHTML = xhr.response['inner']; 
      // document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight  
    }
    else{
      alert("Error en el servidor web")
    }
    };
  }
}); 

// Busca las partes al presionar la lupa de busqeuda
function busqueda_parte(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/lista_partes?"+"parte="+document.getElementById('buscar_parte').value)
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      // document.getElementById('input_nota').value='';;
      tabla_parte.innerHTML = xhr.response['inner']; 
      // document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight  
    }
    else{
      alert("Error en el servidor web")
    }
    };
  }

// Función para asignar parte con la acción seleccionar.   d contiene la id del item
function asignar_parte(a,b,c,d){          
  alert(d)
  // document.getElementById('nombre_parte').textContent=a.nombre_parte.value
  // document.getElementById('referencia').textContent=a.referencia.value
  document.getElementById('nombre_parte').textContent=a;
  document.getElementById('referencia').textContent=b;
  document.getElementById('precio_parte').value=c;
  document.getElementById('id_parte').value=d;
  // Limpia campo ed cantidad
  document.getElementById('cantidad').value = null
}

// Crea una solicitud de parte tra submit
let Solicitud_parte = document.getElementById("form_solicitud_parte");
Solicitud_parte.addEventListener("submit", (e) => {
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/crea_solicitud_parte?"+"servicio="+document.getElementById('num_servicio').value+'&'+
                                                          "nombre_parte="+document.getElementById('nombre_parte').textContent+'&'+
                                                          "referencia="+document.getElementById('referencia').textContent+'&'+
                                                          "precio="+document.getElementById('precio_parte').value+'&'+
                                                          "cantidad="+document.getElementById('cantidad').value+'&'+
                                                          "id_parte="+document.getElementById('id_parte').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']); 
    document.getElementById('tabla_body').innerHTML = xhr.response['inner']; 
    closemodal_modal_solicitud();
    update_mensajes();

  }
  else{
    alert("Error en el servidor web")
  }
  };   
});

// Despliega modal de Eliminar parte de la orden de servicio
function elimina_solicitud_parte(servicio,nombre,referencia,fecha_solicitud,cantidad,precio,total,solicitud_parte){
  // alert(a);
  
  // Carga información
  document.getElementById('servicio_elimina_solicitud').textContent=servicio ;
  document.getElementById('nombre_elimina_solicitud').textContent=nombre;
  document.getElementById('referencia_elimina_solicitud').textContent=referencia ;
  document.getElementById('fecha_elimina_solicitud').textContent=fecha_solicitud ;
  document.getElementById('cantidad_elimina_solicitud').textContent= cantidad;
  document.getElementById('precio_elimina_solicitud').textContent=precio ;
  document.getElementById('total_elimina_solicitud').textContent=total ;
  document.getElementById('solicitud_parte_elimina_solicitud').textContent=solicitud_parte ;
  openmodal_modal_elimina_solicitud_parte();

}

// Elimina parte de la orden de servicio
function elimina_solicitud_accion(){
  // alert('Elminmna')
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/elimina_solicitud_parte?"+"servicio="+document.getElementById('servicio_elimina_solicitud').textContent+'&'+
                                                            "id_solicitud="+document.getElementById('solicitud_parte_elimina_solicitud').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']); 
    document.getElementById('tabla_body').innerHTML = xhr.response['inner']; 
    closemodal_modal_elimina_solicitud_parte();
  }
  else{
    alert("Error en el servidor web")
  }
  };   
}


// Descarga PDF de orden de servicio
function imprime_orden(a){
    window.location.href = "/crear_servicio/imprime_orden_servicio?"+"servicio="+a  
  }



// Despliega modal de Eliminar abono
function eliminar_abono(e){
  // alert(e.servicio.value);
  // Carga información
  document.getElementById('servicio_elimina_abono').textContent=e.servicio.value;
  document.getElementById('fecha_elimina_abono').textContent=e.fecha_abono.value;
  document.getElementById('forma_pago_elimina_abono').textContent=e.medio_de_pago.value;
  document.getElementById('detalle_elimina_abono').textContent=e.detalle.value;
  document.getElementById('valor_elimina_abono').textContent= e.valor_abono.value;
  document.getElementById('identidad_elimina_abono').textContent= e.id;
  openmodal_modal_elimina_abono();

}

// Elimina abono de la orden de servicio
function elimina_abono_accion(){
  // alert('Elminmna')
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/elimina_abono?"+"servicio="+document.getElementById('servicio_elimina_abono').textContent+'&'+
                                                   "id_abono="+document.getElementById('identidad_elimina_abono').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']); 
    document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
    closemodal_modal_elimina_abono();
    update_mensajes();
  }
  else{
    alert("Error en el servidor web")
  }
  };   
}

// Habilita campos para editar la orden de servicio
function editar_servicio(){
  alert('¡Está editando la información del servicio el servicio!');
  // let inputs=document.getElementsByClassName('orden_servicio');
  document.getElementById('save_orden').style.display ='block';
  for (let z = 0; z < document.querySelectorAll(".orden_servicio").length; z++) {
    // document.querySelectorAll(".orden_servicio")[z].setAttribute('readonly')
    document.querySelectorAll(".orden_servicio")[z].style.backgroundColor = "#e0e0e0";
    document.querySelectorAll(".orden_servicio")[z].readOnly = false; 
    document.querySelectorAll(".orden_servicio")[z].disabled = false; 
    // document.getElementById('accion').setAttribute('onclick','editar_contacto()')
  }
}

// Actualiza servicio
function actualiza_servicio(){
  // let inputs=document.getElementsByClassName('orden_servicio');
  document.getElementById('save_orden').style.display ='none';
  for (let z = 0; z < document.querySelectorAll(".orden_servicio").length; z++) {
    // document.querySelectorAll(".orden_servicio")[z].setAttribute('readonly')
    document.querySelectorAll(".orden_servicio")[z].style.backgroundColor = "white";
    document.querySelectorAll(".orden_servicio")[z].readOnly = true; 
    document.querySelectorAll(".orden_servicio")[z].disabled = true; 
    // document.getElementById('accion').setAttribute('onclick','editar_contacto()')
  }
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/actualiza_servicio?"+"servicio="+document.getElementById('servicio_edit').value+'&'+
                                                        "lugar="+document.getElementById('lugar').value+'&'+
                                                        "tipo_servicio="+document.getElementById('tipo_servicio').value+'&'+
                                                        "seguimiento="+document.getElementById('seguimiento').value+'&'+
                                                        "nombre="+document.getElementById('nombre_servicio').value+'&'+
                                                        "identidad="+document.getElementById('identidad_servicio').value+'&'+
                                                        "direccion="+encodeURIComponent(document.getElementById('direccion_servicio').value)+'&'+
                                                        "localidad="+encodeURIComponent(document.getElementById('localidad_servicio').value)+'&'+
                                                        "telefono="+document.getElementById('telefono_servicio').value+'&'+
                                                        "email="+encodeURIComponent(document.getElementById('email_servicio').value)+'&'+
                                                        "marca="+encodeURIComponent(document.getElementById('marca_servicio').value)+'&'+
                                                        "producto="+encodeURIComponent(document.getElementById('producto_servicio').value)+'&'+
                                                        "modelo="+encodeURIComponent(document.getElementById('modelo_servicio').value)+'&'+
                                                        "serie="+encodeURIComponent(document.getElementById('serie_servicio').value)+'&'+
                                                        "doc_ref="+encodeURIComponent(document.getElementById('doc_ref_servicio').value)+'&'+
                                                        "falla="+encodeURIComponent(document.getElementById('falla_servicio').value)+'&'+
                                                        "accesorios="+encodeURIComponent(document.getElementById('accesorios_servicio').value)+'&'+
                                                        "observacion="+encodeURIComponent(document.getElementById('observacion_servicio').value));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);     
    // document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
    // closemodal_modal_elimina_abono();
  }
  else{
    alert("Error en el servidor web")
  }
  };  
}


function load_remision(){
  // console.log(document.getElementById("tabla").rows[0].cells.length);
  // console.log(document.getElementById("tabla").rows[1].cells[0].textContent);
  // console.log(document.getElementById("tabla").rows[0]);
  if (document.getElementById("tabla").rows.length > 1){
    innerHMTL='';
    subtotal=0;
    descuento=0;
    total=0;
    for (let z = 1; z < document.getElementById("tabla").rows.length; z++) {
      subtotal=subtotal+(parseInt(document.getElementById("tabla").rows[z].cells[4].textContent)*parseInt(document.getElementById("tabla").rows[z].cells[3].textContent))     
      total=total+(parseInt(document.getElementById("tabla").rows[z].cells[4].textContent)*parseInt(document.getElementById("tabla").rows[z].cells[3].textContent-descuento))     
      // descuento=descuento+(parseInt(document.getElementById("tabla").rows[z].cells[4].textContent)*parseInt(document.getElementById("tabla").rows[z].cells[3].textContent)*parseInt(document.querySelectorAll(".descuento")[z].value))     
      // descuento=parseInt(document.querySelectorAll(".descuento")[z-1].textContent)
      // alert(document.querySelectorAll(".descuento")[1])
      innerHMTL= innerHMTL+ '<div style="display: flex;">'+
                            '<div class="info_casilla" style="width: 20%;">'+
                                '<div>'+
                                    '<span>Referencia</span>'+
                                '</div>'+
                                '<div>'+
                                    // '<span>'+ document.getElementById("tabla").rows[z].cells[1].textContent +'</span>'+  
                                    '<input style="font-size:large;" type="text" value="'+document.getElementById("tabla").rows[z].cells[1].textContent +'"></input>'+                                   
                                '</div>'+
                            '</div>'+
                            '<div class="info_casilla" style="width: 45%;">'+
                                '<div>'+
                                    '<span>Nombre</span>'+
                                '</div>'+
                                '<div>'+
                                    // '<span>'+ document.getElementById("tabla").rows[z].cells[0].textContent+'</span>'+ 
                                    '<input style="font-size:large;" type="text" value="'+document.getElementById("tabla").rows[z].cells[0].textContent +'"></input>'+
                                '</div>'+
                            '</div>'+
                            '<div class="info_casilla" style="width: 10%;">'+
                                '<div>'+
                                    '<span>V/unitario</span>'+
                                '</div>'+
                                '<div>'+
                                    '<span>'+ document.getElementById("tabla").rows[z].cells[4].textContent+'</span>'+ 
                                '</div>'+
                            '</div>'+
                            '<div class="info_casilla" style="width: 5%;">'+
                                '<div>'+
                                    '<span>Cantidad</span>'+
                                '</div>'+
                                '<div>'+
                                    '<span>'+ document.getElementById("tabla").rows[z].cells[3].textContent+'</span>'+ 
                                '</div>'+
                            '</div>'+
                            '<div class="info_casilla" style="width: 10%;">'+
                                '<div>'+
                                    '<span>Descuento %</span>'+
                                '</div>'+
                                '<div>'+
                                    '<input oninput="update_descuento()" class="descuento" type="number"  style="background-color: rgb(214, 214, 214); cursor: auto;" value="0" placeholder="0"  >'+ 
                                '</div>'+
                            '</div>'+
                            '<div class="info_casilla" style="width: 10%;">'+
                                '<div>'+
                                    '<span>Valor total</span>'+
                                '</div>'+
                                '<div>'+
                                    '<span>'+ document.getElementById("tabla").rows[z].cells[5].textContent+'</span>'+ 
                                    // '<span>'+'100'+'</span>'+ 
                                '</div>'+
                            '</div>'+
                          '</div>'
      }
      document.getElementById('subtotal_remision').textContent='$  '+ subtotal;
      document.getElementById('descuento_remision').textContent='$  '+ descuento;
      document.getElementById('total_remision').textContent='$  '+ total;
      // Creamos HTML con las partes solicitadas en la orden de servicio
      document.getElementById('partes_remision').innerHTML = innerHMTL; 
      // alert(descuento)
      //   document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelectorAll('.sub_sub_item')[z].style.display='inline-block';
    
  }

  openmodal_modal_remision();
}

function ver_remision_existente(){
  openmodal_modal_ver_remision();
}

// Funciones de visualización modal remisión

function forma_pago(){
  if (document.getElementById('tipo_servicio_remision').value=='contado'){
    // alert('asd');
    document.getElementById('medio_pago').style.display = 'block';
    document.getElementById('vencimiento').style.display = 'none';
    document.getElementById('fecha_vencimiento_remision').required = false;
    document.getElementById('medio_pago_remision').required = true;
  }
  else{
    document.getElementById('medio_pago').style.display = 'none';
    document.getElementById('vencimiento').style.display = 'block';
    document.getElementById('fecha_vencimiento_remision').required = true;
    document.getElementById('medio_pago_remision').required = false;
  }
}

//  Actualiza cuando cambian el descuento
function update_descuento(){
  subtotal=0;
  descuento=0;
  total=0;
  for (let z = 0; z < document.querySelectorAll(".descuento").length; z++) {
    // alert(document.querySelectorAll(".descuento")[z].value)
      // descuento=descuento+
      subtotal=subtotal+(parseFloat(document.getElementById("tabla").rows[z+1].cells[5].textContent))     
      descuento=descuento+((parseFloat(document.querySelectorAll(".descuento")[z].value)/100)*parseFloat(document.getElementById("tabla").rows[z+1].cells[5].textContent));
      // total=total+(parseInt(document.getElementById("tabla").rows[z].cells[4].textContent)*parseInt(document.getElementById("tabla").rows[z].cells[3].textContent-descuento)) 
  }
  document.getElementById('subtotal_remision').textContent='$  '+ subtotal;
  document.getElementById('descuento_remision').textContent='$  '+ descuento;
  document.getElementById('total_remision').textContent='$  '+ (subtotal - descuento);
}

// Crea remisión
  let RemisionForm = document.getElementById("forma_remision");
  RemisionForm.addEventListener("submit", (e) => {
  e.preventDefault();
  // Creamos lista con la informacion de partes
  informaciom_partes='';
  

  // let informaciom_partes = {
  // };
  // alert(document.getElementById("tabla").rows[0].cells.length)
  for (let z = 0; z < document.querySelectorAll(".descuento").length; z++) {
    // informaciom_partes=informaciom_partes+'solicitud_parte_fila_'+ z +':{'
    // informaciom_partes=informaciom_partes+'{'+'id:'+'solicitud_parte_fila_'+ z +','
    // let item = {
    // };
    // item['id'] = 'solicitud_parte_fila_'+ z
    for (let i = 0; i < (document.getElementById("tabla").rows[z+1].cells.length - 1); i++) {
      // document.getElementById("tabla").rows[z+1].cells[5].textContent
      // informaciom_partes=informaciom_partes+ document.getElementById("tabla").rows[0].cells[i].textContent+':'+document.getElementById("tabla").rows[z+1].cells[i].textContent+','
      informaciom_partes=informaciom_partes+document.getElementById("tabla").rows[z+1].cells[i].textContent+','
      // alert('asd')
      // item[document.getElementById("tabla").rows[0].cells[i].textContent] = document.getElementById("tabla").rows[z+1].cells[i].textContent;
      
    }
    // informaciom_partes=informaciom_partes+'descuento:'+document.querySelectorAll(".descuento")[z].value+'},'
    // informaciom_partes=informaciom_partes+'descuento:'+document.querySelectorAll(".descuento")[z].value+',divisor_item,'
    informaciom_partes=informaciom_partes+document.querySelectorAll(".descuento")[z].value+',divisor_item'
    // informaciom_partes.push
    // informaciom_partes['solicitud_parte_fila_'+ z]=item
    // alert(item['nombre'])
  // alert(informaciom_partes.keys('nombre').length)  
  }
  // console.log(informaciom_partes.length) 
  // informaciom_partes={"firstName":"John", "lastName":"Doe"}
  // alert('asd')
  const xhr = new XMLHttpRequest();
  // servicio,forma_pago,medio_pago,fecha_vencimiento,producto,marca,identificacion,cliente,direccion,total_abonos,subtotal,descuento,total,usuario
  xhr.open("GET", "/crear_servicio/crea_remision?"+"servicio="+document.getElementById('servicio_remision').textContent+'&'+
                                                   "forma_pago="+document.getElementById('tipo_servicio_remision').value+'&'+
                                                   "medio_pago="+document.getElementById('medio_pago_remision').value+'&'+ 
                                                   "fecha_vencimiento="+document.getElementById('fecha_vencimiento_remision').value+'&'+ 
                                                   "producto="+encodeURIComponent(document.getElementById('producto_remision').textContent)+'&'+ 
                                                   "marca="+encodeURIComponent(document.getElementById('marca_remision').textContent)+'&'+ 
                                                   "identificacion="+document.getElementById('identidad_remision').textContent+'&'+ 
                                                   "cliente="+encodeURIComponent(document.getElementById('cliente_remision').textContent)+'&'+ 
                                                   "direccion="+encodeURIComponent(document.getElementById('direccion_remision').textContent)+'&'+ 
                                                   "total_abonos="+encodeURIComponent(document.getElementById('total_abonos_remision').textContent)+'&'+ 
                                                   "subtotal="+encodeURIComponent(document.getElementById('subtotal_remision').textContent)+'&'+ 
                                                   "descuento="+(document.getElementById('descuento_remision').textContent)+'&'+
                                                   "informacion_parte="+encodeURIComponent(informaciom_partes)+'&'+    
                                                   "total="+encodeURIComponent(document.getElementById('total_remision').textContent));
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    // closemodal_asignar_tecnico();
    alert(xhr.response['message']); 
    closemodal_modal_remision();
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio_edit').value; 
    update_remision();
    update_mensajes()
    // if ("El técnico fue asignado"==xhr.response['message']){
    //   document.getElementById('tecnico').textContent = document.getElementById('lista_tecnicos').options[document.getElementById('lista_tecnicos').selectedIndex].text;
    // } 
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});


// Elimina remisión
function elimina_remision(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/elimina_remision?"+"servicio="+document.getElementById('servicio_edit').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);   
    closemodal_modal_ver_remision(); 
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio_edit').value; 
    update_mensajes();
    update_remision();
    // document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
    // closemodal_modal_elimina_abono();
  }
  else{
    alert("Error en el servidor web")
  }
  };  
}

// Descarga PDF de remisión
function imprime_remision(a){
  window.location.href = "/crear_servicio/imprime_remision?"+"servicio="+a  
}

// Asigna estado tras submit button
let AsignaEstadoForm = document.getElementById("form_asigna_estado");
AsignaEstadoForm.addEventListener("submit", (e) => {
  // alert(document.getElementById('lista_estados').value)
  e.preventDefault();
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/crea_estado?"+"servicio="+document.getElementById('numero_servicio').value+'&'+
                                                 "tecnico="+document.getElementById('tecnico').textContent+'&'+
                                                 "estado="+document.getElementById('lista_estados').value);
                                                    // "estado="+'asignación');
  // const xhr = new XMLHttpRequest();
  // xhr.open("GET", "/crear_servicio/crea_estado?"+"entity="+document.getElementById('numero_servicio').value+'&'+
  //                                                   "user="+document.getElementById('lista_tecnicos').value);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    // closemodal_asignar_tecnico();
    alert(xhr.response['message']); 
    closemodal_asignar_estado();
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio').textContent;
    update_estado_panel();
    update_mensajes();


    // if ("El estado fue asignado"==xhr.response['message']){
    //   // document.getElementById('tecnico').textContent = document.getElementById('lista_tecnicos').options[document.getElementById('lista_tecnicos').selectedIndex].text;
    // } 
  }
  else{
    alert("Error en el servidor web")
  }
  };   
});

// Elimina estado
function elimina_estado(a){
  document.getElementById('estado_elimina_estado').textContent=a.estado.value ;
  document.getElementById('tecnico_elimina_estado').textContent=a.tecnico.value ;
  document.getElementById('fecha_elimina_estado').textContent=a.fecha_estado.value.split('T')[0] ;
  document.getElementById('usuario_elimina_estado').textContent=a.usuario.value ;
  document.getElementById('entidad_elimina_estado').textContent=a.id;
  openmodal_modal_elimina_estado();
}

function elimina_estado_accion(){
    const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/elimina_estado?"+"servicio="+document.getElementById('servicio_edit').value+'&'+
                                                    "id_estado="+document.getElementById('entidad_elimina_estado').textContent);
                                      
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);   
    closemodal_modal_elimina_estado(); 
    // window.location.href = "/crear_servicio/ver_servicio?" +"servicio="+document.getElementById('servicio_edit').value; 
    update_mensajes();
    update_estado_panel();
    // document.getElementById('tabla_abonos_detalle').innerHTML = xhr.response['inner']; 
    // closemodal_modal_elimina_abono();
  }
  else{
    alert("Error en el servidor web")
  }
  };   
}

// Actualiza panel de mensajes

function update_mensajes(){
    var div_mensajes = document.getElementById("div_mensajes");
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/crear_servicio/update_mensaje?"+"servicio="+document.getElementById('servicio').textContent);
    xhr.send();
    xhr.responseType = "json"; 
    xhr.onload = () => {
    if (xhr.status==200){
      // document.getElementById('input_nota').value='';
      div_mensajes.innerHTML = xhr.response['mensajes_html']; 
      document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight  
    }
    else{
      alert("Error en el servidor web")
    }
    };
}

// Actualiza panel de remisón

function update_remision(){
  // var div_mensajes = document.getElementById("div_mensajes");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/update_remision?"+"servicio="+document.getElementById('servicio').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){  
    
    document.getElementById('servicio_ver_remision').textContent=xhr.response['servicio_ver_remision'];

    document.getElementById('partes_ver_remision').innerHTML=xhr.response['hmtl_remision'];
    document.getElementById('total_remision_front').textContent=xhr.response['total_remision'];
    document.getElementById('texto_boton_remision_front').textContent=xhr.response['texto_boton_remision'];
    document.getElementById('boton_remision_front').setAttribute('onclick',xhr.response['funcion_boton_remision'])

    document.getElementById('tipo_servicio_ver_remision').textContent=xhr.response['forma_pago_ver_remision']
    document.getElementById('medio_pago_ver_remision_span').textContent=xhr.response['medio_pago_ver_remision']
    document.getElementById('vencimiento_ver_remision_span').textContent=xhr.response['fecha_vencimiento_ver_remision']
    document.getElementById('servicio_ver_remision').textContent=xhr.response['servicio_ver_remision']
    document.getElementById('producto__ver_remision').textContent=xhr.response['producto_ver_remision']
    document.getElementById('marca_ver_remision').textContent=xhr.response['marca_ver_remision']
    document.getElementById('total_abonos_ver_remision').textContent=xhr.response['total_abonos_ver_remision']

    document.getElementById('identidad_ver_remision').textContent=xhr.response['identidad_ver_remision']
    document.getElementById('cliente_ver_remision').textContent=xhr.response['nombre_ver_remision']
    document.getElementById('direccion_ver_remision').textContent=xhr.response['direccion_ver_remision']

    document.getElementById('subtotal_ver_remision').textContent=xhr.response['subtotal_ver_remision']
    document.getElementById('descuento_ver_remision').textContent=xhr.response['descuento_ver_remision']
    document.getElementById('total_ver_remision').textContent=xhr.response['total_ver_remision']

    if (document.getElementById('tipo_servicio_ver_remision').textContent == 'contado'){
      document.getElementById('medio_pago_ver_remision').style.display = 'block';
      document.getElementById('vencimiento_ver_remision').style.display = 'none';
    } 
    else{
      document.getElementById('medio_pago_ver_remision').style.display = 'none';
      document.getElementById('vencimiento_ver_remision').style.display = 'block';
    }

    // document.getElementById('input_nota').value='';
    // div_mensajes.innerHTML = xhr.response['mensajes_html']; 
    // document.getElementById('div_mensajes').scrollTop = document.getElementById('div_mensajes').scrollHeight 

  }
  else{
    alert("Error en el servidor web")
  }
  };
}


// Actualiza panel de estados

function update_estado_panel(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/crear_servicio/update_estado_panel?"+"servicio="+document.getElementById('servicio').textContent);
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){  
    document.getElementById('estados_tabla').innerHTML=xhr.response['estados_html'];
  }
  else{
    alert("Error en el servidor web")
  }
  };
}











