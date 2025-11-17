# 💬 Tornado React Chat App

A **modern real-time chat application** with a Tornado backend and React frontend 🚀. Connect, chat, and have fun in real-time! 😎

## ✨ Features

- ⚡ Real-time messaging using **WebSocket**
- 🏠 Multiple **chat rooms**
- 👤 **User registration on the fly** (enter your username to start)
- 💾 Stores messages in a **MySQL database**
- ⌨️ **Typing indicators** show who is currently typing
- 🎨 Frontend built with **React** and **CSS**
- 🎭 Animated titles using **Shuffle.js**
- ✨ **Glare hover effects** on buttons
- 📜 Smooth scroll and animation for chat messages
- 📨 Sent messages appear on the **right**, received on the **left**

## 🛠 Requirements

- Python 3.8+
- MySQL Server 🐬
- Node.js & npm
- Python packages: `pip install -r requirements.txt`
- React dependencies: `npm install` in `frontend/` folder

## 🚀 Setup
2️⃣ Backend Setup


Install Python dependencies:


pip install -r requirements.txt



Configure your MySQL database and update db.py with credentials 🔑.


Start the Tornado server:


python app.py

The backend runs on http://localhost:8888 🌐.
3️⃣ Frontend Setup


Navigate to the frontend folder:


cd frontend



Install dependencies:


npm install



Start the React server:


npm start

The frontend runs on http://localhost:3000 🎉.
💡 Usage


Open the app in your browser 🌍.


Enter your username and room name to join or create a chat room 🏠.


Start chatting in real-time with others 💬.


See typing indicators for live updates ⌨️.


Sent messages appear on the right, received messages on the left ↔️.


📁 File Structure


app.py: Tornado server & WebSocket handler 🐍


db.py: MySQL database connection 💾


frontend/: React frontend ⚛️


ChatContainer.css: Styling for chat interface 🎨


GlareHover.js & Shuffle.js: Frontend UI effects ✨


📜 License
MIT License 📝



### 1️⃣ Clone the repository
```bash
git clone https://github.com/DhiaMejdi/chat-app.git
cd chat-app

