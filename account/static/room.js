function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + 'kl' + "/");
    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }
    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
 
    chatSocket.onmessage = function(e) {
        msg = JSON.parse(e.data).message
        var message_block = document.getElementById('custom-message-extension')
        var li_node = document.createElement("LI");
        li_node.classList.add('success', 'success-msg');
        li_node.textContent = msg
        message_block.appendChild(li_node)
    };
    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();
