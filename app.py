import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime
import logging
from db import get_connection

clients = {}

logging.basicConfig(level=logging.INFO)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("http://localhost:3000")

class ChatWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.username = None
        self.room = None
        self.write_message("CONNECTED_OK")

    def on_message(self, message):

        # typing event
        if message.startswith("TYPING|"):
            _, username, room = message.split("|", 2)
            if room in clients:
                for c in clients[room]:
                    if c != self:
                        c.write_message(f"TYPING|{username}")
            return

        # normal message
        username, room, text = message.split("|", 2)
        self.username = username
        self.room = room

        if room not in clients:
            clients[room] = set()
        clients[room].add(self)

        full = f"{username}|{room}|{text}"

        for c in list(clients[room]):
            try:
                c.write_message(full)
            except:
                clients[room].remove(c)

    def on_close(self):
        if self.room in clients and self in clients[self.room]:
            clients[self.room].remove(self)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", ChatWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server running on 8888")
    tornado.ioloop.IOLoop.current().start()
