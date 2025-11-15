# 🗨️ Tornado Chat App -- Complete Documentation

A fully functional real-time chat application built using **Tornado
WebSockets**, **MySQL**, HTML/CSS/JS, and Python.

This README includes: - Full features overview
- Installation steps
- Database setup
- Project structure
- How to run
- How to test
- Troubleshooting
- Future improvements

------------------------------------------------------------------------

# 🚀 Features

-   ⚡ Real-time chat using WebSockets
-   🏠 Multiple chat rooms
-   👤 Auto-user creation
-   🗃️ Messages stored in MySQL
-   🔌 Tornado non-blocking server
-   🎨 Lightweight frontend
-   🧩 Easy to modify and extend

------------------------------------------------------------------------

# 📦 Requirements

Your machine must have:

### **Software**

-   Python **3.8+**
-   MySQL Server (8 recommended)
-   Git (optional)

------------------------------------------------------------------------

# 🛠️ Installation Guide --- Step by Step

## ✅ 1. Clone the project

``` bash
git clone https://github.com/DhiaMejdi/chat-app.git
cd chat-app
```

------------------------------------------------------------------------

## ✅ 2. Install dependencies

``` bash
pip install -r requirements.txt
```

If you're using PowerShell:

``` powershell
py -m pip install -r requirements.txt
```

------------------------------------------------------------------------

## ✅ 3. Create and Configure MySQL Database

### Open MySQL console:

``` bash
mysql -u root -p
```

### Run these SQL commands:

``` sql
CREATE DATABASE chatapp;

CREATE USER 'chatuser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON chatapp.* TO 'chatuser'@'localhost';
FLUSH PRIVILEGES;

USE chatapp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

------------------------------------------------------------------------

## ✅ 4. Update Database Configuration (if needed)

`db.py` file:

``` python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chatuser",
        password="password123",
        database="chatapp"
    )
```

Change user/password if your MySQL setup differs.

------------------------------------------------------------------------

# ▶️ Running the Application

Inside the project folder, run:

``` bash
python app.py
```

Or on PowerShell:

``` powershell
py app.py
```

If successful, you will see:

    📂 Static files served from: C:/.../chat-app/static
    🚀 Tornado chat server running on http://localhost:8888

Now open:

👉 http://localhost:8888

------------------------------------------------------------------------

# 💬 How to Use the Chat

Messages must follow this format:

    username | room | message

Example:

    Ali|general|Hello world!
    Sarah|dev|Welcome to the dev room 🚀

------------------------------------------------------------------------

# 📁 Project Structure

    chat-app
    │── static
    │   ├── script.js
    │   └── style.css
    │── templates
    │   └── index.html
    │── app.py
    │── db.py
    │── requirements.txt
    │── README.md

------------------------------------------------------------------------

# 🧪 Testing

Open two browser tabs:

    http://localhost:8888

Join the same room:

    Ali|general|Hello
    Mejdi|general|Hi Ali

Messages should appear in real-time.

------------------------------------------------------------------------

# 🐞 Troubleshooting

### ❌ `mysql` is not recognized

MySQL is not installed or not added to PATH.

### ❌ Database connection error

Check your credentials in `db.py`.

### ❌ WebSocket not connecting

Ensure frontend uses:

    ws://localhost:8888/ws

### ❌ pip not recognized

Use:

``` powershell
python -m pip install tornado
```

------------------------------------------------------------------------

# 🔧 Future Enhancements

-   JSON-based WebSocket protocol
-   Modern chat UI 
-   Docker + docker-compose (App + MySQL)
-   Admin message panel
-   REST API for rooms and users
-   Multi-room UI with user list

------------------------------------------------------------------------