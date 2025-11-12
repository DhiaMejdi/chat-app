let ws = null;

document.getElementById("joinBtn").addEventListener("click", () => {
    const username = document.getElementById("username").value.trim();
    const room = document.getElementById("room").value.trim();

    if (!username || !room) {
        alert("Please enter both username and room name!");
        return;
    }

    ws = new WebSocket(`ws://${window.location.host}/ws`);

    ws.onopen = () => {
        console.log("Connected to server");
        document.querySelector(".user-setup").classList.add("hidden");
        document.getElementById("chat-section").classList.remove("hidden");
        appendMessage("✅ Connected to chat server!");
    };

    ws.onmessage = (event) => {
        appendMessage(event.data);
    };

    ws.onclose = () => {
        appendMessage("❌ Disconnected from server.");
    };

    document.getElementById("sendBtn").onclick = () => sendMessage(username, room);
    document.getElementById("message").addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage(username, room);
    });
});

function sendMessage(username, room) {
    const msgInput = document.getElementById("message");
    const text = msgInput.value.trim();
    if (!text || !ws) return;
    ws.send(`${username}|${room}|${text}`);
    msgInput.value = "";
}

function appendMessage(text) {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = "message";
    div.textContent = text;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}
