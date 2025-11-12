import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime
import logging
import os
from db import get_connection

# ======================
# Global state
# ======================
clients = {}  # {room_name: set of WebSocketHandler instances}

# ======================
# Configure logging
# ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ======================
# Request Handlers
# ======================
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

# ======================
# WebSocket Handler
# ======================
class ChatWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        """Allow CORS for local testing (adjust in production)."""
        return True

    def open(self):
        """Triggered when a new WebSocket client connects."""
        self.username = None
        self.room_name = None
        logging.info("New WebSocket connection opened.")
        self.write_message("✅ Connected to the chat server!")

    def on_message(self, message):
        """Handle incoming WebSocket messages."""
        try:
            username, room_name, text = message.split("|", 2)
        except ValueError:
            self.write_message("❌ Invalid message format. Use: username|room|message")
            return

        self.username = username.strip()
        self.room_name = room_name.strip()
        text = text.strip()

        # Ensure room exists in clients dictionary
        if self.room_name not in clients:
            clients[self.room_name] = set()
        clients[self.room_name].add(self)

        # Save message to DB safely
        try:
            self.save_message(self.username, self.room_name, text)
        except Exception as e:
            logging.error(f"Database error:\n{e}")
            self.write_message("❌ Error saving message.")
            return

        # Broadcast message to all clients in the same room
        formatted_msg = f"[{self.room_name}] {self.username}: {text}"
        for client in list(clients[self.room_name]):  # iterate over a copy
            try:
                client.write_message(formatted_msg)
            except tornado.websocket.WebSocketClosedError:
                clients[self.room_name].remove(client)

    def save_message(self, username, room_name, text):
        """Insert user, room, and message into the database."""
        conn = get_connection()
        cursor = conn.cursor()

        # Ensure user exists
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if not user:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            conn.commit()
            user_id = cursor.lastrowid
        else:
            user_id = user[0]

        # Ensure room exists
        cursor.execute("SELECT id FROM rooms WHERE name=%s", (room_name,))
        room = cursor.fetchone()
        if not room:
            cursor.execute("INSERT INTO rooms (name) VALUES (%s)", (room_name,))
            conn.commit()
            room_id = cursor.lastrowid
        else:
            room_id = room[0]

        # Insert message
        cursor.execute("""
            INSERT INTO messages (room_id, user_id, message, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (room_id, user_id, text, datetime.datetime.now()))
        conn.commit()

        cursor.close()
        conn.close()

    def on_close(self):
        """Triggered when a client disconnects."""
        if self.room_name in clients and self in clients[self.room_name]:
            clients[self.room_name].remove(self)
            logging.info(f"User {self.username} left room {self.room_name}")
        else:
            logging.info("WebSocket connection closed.")


# ======================
# App setup
# ======================
def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", ChatWebSocket),
        ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )


if __name__ == "__main__":
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    print(f"📂 Static files served from: {static_dir}")
    app = make_app()
    app.listen(8888)
    logging.info("🚀 Tornado chat server running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
