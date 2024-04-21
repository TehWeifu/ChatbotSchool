document.getElementById('user-input').addEventListener('submit', function (event) {
    event.preventDefault();
    sendMessage();
});

function sendMessage() {
    const userMessage = document.getElementById('user-message').value;
    const chatDisplay = document.getElementById('chat-display');
    // Mostrar el mensaje del usuario en el chat display
    chatDisplay.innerHTML += '<p class="user"><strong>Tú:</strong> ' + userMessage + '</p>';
    // Enviar mensaje al servidor de Rasa y obtener la respuesta
    fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: userMessage}),
    })
        .then(response => response.json())
        .then(data => {
            // Mostrar la respuesta de Rasa en el chat display
            chatDisplay.innerHTML += '<p class="rasa"><strong>Chatbot:</strong> ' + data[0].text + '</p>';
        });
    // Limpiar el input de usuario
    document.getElementById('user-message').value = '';
}
