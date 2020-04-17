import tornado.ioloop
import tornado.web
import multiprocessing
import tornado.httpserver

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    count = multiprocessing.cpu_count()
    print("cpu count %s" % count)
    app = make_app()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(9999)
    http_server.start(count)
    tornado.ioloop.IOLoop.instance().start()