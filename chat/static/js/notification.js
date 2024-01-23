const websocketNotification = new WebSocket('ws://' + window.location.host + '/ws/notification/');

websocketNotification.onopen = function () {
    console.log('notification connected');
}

websocketNotification.onmessage = function (event) {
    console.log(event.data);
    let count = document.querySelector('#count');
    try {
        let data = JSON.parse(event.data);
        if (data.type === 'initial_notification_count') {
            // Handle the initial notification count
            count.innerHTML = data.count;
            console.log('Initial Notification Count:', data.count);
        } else {
            // Handle other types of messages
            console.log(data.count);
        }
    } catch (error) {
        console.error('Error parsing notification data:', error);
    }
};


websocketNotification.onclose = function () {
    console.log('websocket closed');
}
