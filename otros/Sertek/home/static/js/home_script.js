const menu = document.getElementById("icon_action");
const barra_lateral=document.getElementById("barra_lateral");

setInterval(message, 10000);

function message() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/mensajes/get_global_message");                                
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    // alert(xhr.response['global_message'])
    document.getElementById('message').innerHTML= xhr.response['global_message'] 
  }
  else{
    document.getElementById('message').innerHTML= '                                        '
  }
  };
}


menu.addEventListener("click",()=>{ 
  if (barra_lateral.offsetWidth==245) {
    barra_lateral.style.width="0px";
    document.getElementById("contenido").style.width="100%";
    document.getElementById("contenido").style.marginLeft="0px";
  
  // while (document.getElementById("contenido").style.marginLeft != "0px") {
    
  // }
  // document.getElementById("contenido").style.width="100hv";
  // barra_lateral.style.visibility="hidden"; 
  }
  else{
    barra_lateral.style.width="245px";
      document.getElementById("contenido").style.marginLeft="245px";
      document.getElementById("contenido").style.width="width: calc(100% - var(--ancho_barra_lateral))";
      // barra_lateral.style.visibility="visible";
  }
});

// console.log(document.querySelectorAll(".item_lista_lateral").length);
// console.log(document.querySelectorAll(".item_lista_lateral")[0].querySelector(".sub_lista"));
// (function(index){alert(index)})(4);


for(let i = 0; i < document.getElementsByClassName('item_lista_lateral').length; i++) {
  (function(index) {
    document.getElementsByClassName('icon_span')[index].addEventListener("click", function() {
      //  console.log("Clicked index: " + index);
       if (index != 0 && index !=5 && index !=6 )
       {   
        //  alert(document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_item").style.display);
          // if (document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_item").style.display==""){
          //   console.log("none");
          //   // alert(document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_item").style.display);
          // }
          
       if (document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_item").style.display=="inline-block"){
            for (let z = 0; z < document.querySelectorAll(".item_lista_lateral")[index].querySelectorAll(".sub_item").length; z++) {
              document.querySelectorAll(".item_lista_lateral")[index].querySelectorAll(".sub_item")[z].style.display="none";
            }
            // document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_lista").style.display="none";
            // document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_lista").style.position="relative";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector("span").style.color= "rgba(0, 0, 0, 0.87)";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector("span").style.transform="scale(1)";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector(".flecha_submenu").style.transform="rotate(0deg)";
        }
        else{
            for (let q = 0; q < document.querySelectorAll(".item_lista_lateral")[index].querySelectorAll(".sub_item").length; q++) {
              document.querySelectorAll(".item_lista_lateral")[index].querySelectorAll(".sub_item")[q].style.display="inline-block";
              // console.log(q);
            }
            // document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_lista").style.display="inline-block";
            // document.querySelectorAll(".item_lista_lateral")[index].querySelector(".sub_lista").style.position="absolute";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector("span").style.color="rgb(21, 101, 192)";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector("span").style.transform="scale(1.1)";
            document.querySelectorAll(".item_lista_lateral")[index].querySelector(".flecha_submenu").style.transform="rotate(180deg)";
        }   
      } 
     })
  })(i);
}

for(let i = 0; i < document.querySelectorAll('.item_lista_lateral').length; i++) 
  {
    for(let x = 0; x < document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item').length; x++) 
    { 
      // console.log(i,document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item').length);
      // console.log(i,x);
      // for (let y = 0; y < document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[x].querySelectorAll('.sub_sub_item').length; y++) 
      // {
        // console.log(i,x);
        (function(index) {
          document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_icon_span')[index].addEventListener("click", function() {
            //  console.log("Clicked index: " + index); 
            //  console.log(document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('span').style.color)
            //  console.log(document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('.flecha_sub_submenu').display. )
            if(document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('span').style.color != "rgb(21, 101, 192)" ){
              document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('span').style.color="rgb(21, 101, 192)";
              document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('.flecha_sub_submenu').style.transform="rotate(180deg)";
              // document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('span').style.color="rgba(0, 0, 0, 0.8)";
              // document.querySelectorAll('.item_lista_lateral')[i].querySelector('.sub_lista').style.position='absolute';
              for (let z = 0; z < document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelectorAll('.sub_sub_item').length; z++) {
                document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelectorAll('.sub_sub_item')[z].style.display='inline-block';
              }
              
              
            }
            else{
              document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('span').style.color="rgba(0, 0, 0, 0.8)";
              document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('.flecha_sub_submenu').style.transform="rotate(0deg)";
              // document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelector('.sub_sub_item').style.display='none';
              for (let z = 0; z < document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelectorAll('.sub_sub_item').length; z++) {
                document.querySelectorAll('.item_lista_lateral')[i].querySelectorAll('.sub_item')[index].querySelectorAll('.sub_sub_item')[z].style.display='none';
              }
            }
             
           })
        })(x);

      // }
    } 
  }

function cambio_ciudad(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/home/cambio_ciudad?"+"ciudad="+document.getElementById('ciudad').value );                                
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    alert(xhr.response['message']);
    get_ciudad_actual();   
  }
  else{
    alert("Error en el servidor web")
  }
  };   
}

function get_ciudad_actual(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "/home/ciudad_actual");                                
  xhr.send();
  xhr.responseType = "json"; 
  xhr.onload = () => {
  if (xhr.status==200){
    document.getElementById('ciudad').innerHTML= xhr.response['lista_ciudades'] 
  }
  else{
    alert("Error en el servidor web")
  }
  };
}

function set_iframe(url){
  document.getElementById('iframe_contenido').src = url;
}






