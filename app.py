import tornado.ioloop
import tornado.web
import tornado.websocket
from db import get_connection
import datetime
import os

clients = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

class ChatWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.add(self)
        # Load last 50 messages from DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.username, r.name, m.message, m.timestamp
            FROM messages m
            JOIN users u ON m.user_id = u.id
            JOIN rooms r ON m.room_id = r.id
            ORDER BY m.timestamp DESC LIMIT 50
        """)
        messages = cursor.fetchall()
        for username, room, message, timestamp in reversed(messages):
            self.write_message(f"[{room}] {username}: {message}")
        cursor.close()
        conn.close()

    def on_message(self, message):
        try:
            username, room_name, text = message.split("|", 2)
        except ValueError:
            return  # ignore malformed messages

        # Save message to DB
        conn = get_connection()
        cursor = conn.cursor()

        # Get user id
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user:
            user_id = user[0]
        else:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            conn.commit()
            user_id = cursor.lastrowid

        # Get room id
        cursor.execute("SELECT id FROM rooms WHERE name=%s", (room_name,))
        room = cursor.fetchone()
        if room:
            room_id = room[0]
        else:
            cursor.execute("INSERT INTO rooms (name) VALUES (%s)", (room_name,))
            conn.commit()
            room_id = cursor.lastrowid

        # Insert message
        cursor.execute("""
            INSERT INTO messages (room_id, user_id, message)
            VALUES (%s, %s, %s)
        """, (room_id, user_id, text))
        conn.commit()
        cursor.close()
        conn.close()

        # Broadcast to all clients
        for client in clients:
            client.write_message(f"[{room_name}] {username}: {text}")

    def on_close(self):
        clients.remove(self)

# === Fix static files path here ===
app = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/ws", ChatWebSocket),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static")  # <--- mouhem jeddan jeddan
)

if __name__ == "__main__":
    print("Static files served from:", os.path.join(os.path.dirname(__file__), "static"))
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
