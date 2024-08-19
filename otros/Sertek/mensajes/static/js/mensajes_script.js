// Función para agregar un mensaje al cuadro de mensajes
function addMessage(message) {
    const messageBox = document.getElementById('message-box');
    // Limpiamos campo para que solo quede el último mensaje
    messageBox.textContent=' '
    const p = document.createElement('p');
    p.textContent = message;
    messageBox.appendChild(p);
}

// Función para insertar un emoji en el área de texto
function insertEmoji(emoji) {
    const messageInput = document.getElementById('message');
    messageInput.value += emoji;
    messageInput.focus();
}

// Manejador de envío del formulario
document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (message !== '') {
        
        // Setea el mensaje en el servidor 
        const xhr = new XMLHttpRequest();
        xhr.open("GET","/mensajes/set_global_message?"+"mensaje_global="+encodeURIComponent(document.getElementById('message').value));
        xhr.send();
        xhr.responseType = "json"; 
        xhr.onload = () => {
        if (xhr.status==200){
            alert(xhr.response['message'])    
        }
        else{
            alert("Error en el servidor web")
        }
        };

        addMessage(message);
        messageInput.value = '';
        messageInput.focus();
    } else {
        alert('Ingrese un mensaje válido.');
    }
});






