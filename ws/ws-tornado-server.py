import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import json

sockets = {}


class EchoHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "open"


    def on_close(self):
        print "close"

    def on_message(self, message):
        print "message"
        m = json.loads(message)
        if m['type'] == 'hello':
            sockets[m['id']] = self
            print sockets
        else:
            sockets[m['id']].write_message(message)
        
        self.write_message("message")

    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/ws", EchoHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()