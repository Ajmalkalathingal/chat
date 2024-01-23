const usernameElement = document.getElementById('json-message-username');
const loginUser = JSON.parse(usernameElement.textContent);

const websocketOnline = new WebSocket('ws://'+ window.location.host +'/ws/online/');

// only user in live in connect
websocketOnline.onopen = function(event) {
    console.log('WebSocket connection online opened');
    websocketOnline.send(JSON.stringify({
        'username' : loginUser,
        'type':'open'
    })
    )
};

window.addEventListener('beforeunload',function(e){
    websocketOnline.send(JSON.stringify({
        'username': loginUser,
        'type':'offline'
    }))
})

websocketOnline.onmessage = function(event){
    // console.log('data', event)
    let data = JSON.parse(event.data)
    // console.log('user status',data.status, 'username', data.username)

    // if(data.username != loginUser){}
    let status_color = document.getElementById(`${data.username}_status`)
    let online_ofline = document.getElementById(`${data.username}online`)

        if(data.status == true){
            status_color.style.color='green';
            online_ofline.textContent='online';
        }
        else{
            status_color.style.color='grey';
            online_ofline.textContent='Ofline';
        }
    }


websocketOnline.onerror = function(event) {
    console.error('WebSocket error:');
};

websocketOnline.onclose = function(event){
    console.log('closed',event)
}