import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import json

sockets = {}    # {username: Handler}


class Handler(tornado.websocket.WebSocketHandler):

    def on_hello(self, msg):
        sockets[msg['username']] = self
        print sockets

    def on_bye(self, msg):
        del sockets[msg['username']]
        print "bye", sockets

    msg_types = {
        'hello': on_hello,
        'bye': on_bye,
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
        print "message"
        m = json.loads(message)
        self.msg_types[m['type']](self, m)

        # if m['type'] == 'hello':
        #     sockets[m['id']] = self
        #     print sockets
        # else:
        #     sockets[m['id']].write_message(message)

    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/ws", Handler),
    ])
    app.listen(8880)
    tornado.ioloop.IOLoop.instance().start()