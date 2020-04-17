from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from multiprocessing import cpu_count, Process,Manager

app = Flask(__name__)
server = WSGIServer(('0.0.0.0', 6000), app, log=None)
server.start()

handler = RotatingFileHandler('app.log',encoding='UTF-8',maxBytes=1024*1024*10,backupCount=20)
# handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route('/',methods=['POST','GET'])
def hello():
    return 'hello world'

def serve_forever():
    global server
    server.start_accepting()
    server._stop_event.wait()

if __name__ == "__main__":
    count = cpu_count()
    print("cpu count %s" % count)
    for i in range(count):
        p = Process(target=serve_forever)
        p.start()