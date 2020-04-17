from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

handler = RotatingFileHandler('app.log',encoding='UTF-8',maxBytes=1024*1024*10,backupCount=20)
# handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route('/',methods=['POST','GET'])
def hello():
    return 'hello world'

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()

    app.debug = True
    # app.run(host='0.0.0.0', port=5000)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()