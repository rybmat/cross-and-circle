import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import json

sockets = {}    # {username: Handler}

pending_msgs = {}

class Handler(tornado.websocket.WebSocketHandler):

    def on_hello(self, msg):
        sockets[msg['username']] = self
        for m in pending_msgs.get(msg['username'], []):
            self.write_message(m)
        if pending_msgs.get(msg['username'], False):
            del pending_msgs[msg['username']]
        print sockets

    def on_bye(self, msg):
        del sockets[msg['username']]
        print "bye", sockets

    def route(self, msg):
        handler = sockets.get(msg['to'], None)
        if handler:
            handler.write_message(msg)
        else:
            pending_msgs.setdefault(msg['to'], []).append(msg)


    msg_types = {
        'hello': on_hello,
        'bye': on_bye,
        'move': route,
        'req-acc': route,
        'new-req': route,
    }

    def open(self):
        print "open"


    def on_close(self):
        u = ''
        for k, v in sockets.iteritems():
            if v == self:
                u = k
                break
        if u:
            del sockets[u]

        print "close"

    def on_message(self, message):
        print "message", message
        m = json.loads(message)
        self.msg_types[m['type']](self, m)


    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/ws", Handler),
    ])
    app.listen(8880)
    tornado.ioloop.IOLoop.instance().start()