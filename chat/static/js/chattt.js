const user_name = JSON.parse(document.getElementById('json-username').textContent)
const user_message = JSON.parse(document.getElementById('json-message-username').textContent)
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent)
// console.log(user_name)
// console.log(user_message)

const websocket = new WebSocket('ws://' + window.location.host +'/ws/'+ user_name + '/');

websocket.onopen = function(e){
    console.log('websocket connected chat')
}

websocket.onclose = function(e){
    console.log('conection closed')
}

websocket.onerror = function(e){
    console.log('error',)
}

websocket.onmessage = function(event){
    // console.log('message',event)
    // console.log(event.data)
    let data = JSON.parse(event.data)
    console.log(data.receiver)

if (data.username === user_message) {
    document.querySelector('#chat-body').innerHTML += `
    <tr>
        <td>
            <p class="p-2 mt-2 rounded">
                <span class="bg-primary p-2 text-white rounded">${data.message}</span>
            </p>
        </td>
    </tr>
`;
} else {
    document.querySelector('#chat-body').innerHTML += `
        <tr>
            <td> 
                <p p-2 mt-2 rounded">
                    <span class="bg-success p-2 text-white rounded">${data.message}</span>
                </p>
            </td>
        </tr>
    `;
}

}

document.getElementById('chat-message-submit').onclick = function(e) {
let message_input = document.getElementById('message_input');
const message = message_input.value;
// console.log(message)

if (message.trim() !== '') {
    websocket.send(JSON.stringify({
        'message': message,
        'username': user_message,
        'receiver' :receiver
    }));
}

message_input.value = '';
};