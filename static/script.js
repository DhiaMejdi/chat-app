// Connect to WebSocket
let ws = new WebSocket("ws://" + window.location.host + "/ws");

// Listen for incoming messages
ws.onmessage = function(event) {
    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += event.data + "<br>";
    chatbox.scrollTop = chatbox.scrollHeight;
};

// Send message when clicking "Send"
function sendMessage() {
    let username = document.getElementById("username").value.trim();
    let room = document.getElementById("room").value.trim();
    let message = document.getElementById("message").value.trim();

    if(username && room && message){
        // Format: username|room|message
        ws.send(username + "|" + room + "|" + message);
        document.getElementById("message").value = "";
    } else {
        alert("Please enter username, room, and message.");
    }
}
