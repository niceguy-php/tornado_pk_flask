# -*- coding: UTF-8 -*-
import hmac
import requests
import base64
import hashlib
import time
import traceback
import datetime
KEY_AUTH = 'block90'

HOST = 'http://hello.com/hello'
HMAC_USERNAME = 'user1'
HMAC_SECRET = "123456"
BASIC_AUTH = 'Basic dmlyY2xlOjk5OTAwMA=='
#from https://www.cnpython.com/pypi/httpie-kong-hmac
class KongHMAC:
    def __init__(self, username, password, algorithm='hmac-sha256',
                 headers=['request-line', 'date'], charset='utf-8'):
        self.username = username
        self.password = password
        self.algorithm = algorithm
        self.headers = headers
        self.charset = charset

        self.auth_template = 'hmac username="{}", algorithm="{}", headers="{}", signature="{}"'

    def __call__(self, r):
        try:

            # add Date header
            if 'date' in self.headers and 'Date' not in r.headers:
                r.headers['Date'] = self.create_date_header()

            # add Digest header
            if r.body:
                r.headers['Digest'] = 'SHA-256={}'.format(self.get_body_digest(r))
                if 'digest' not in self.headers:
                    self.headers.append('digest')

            # get sign
            sign = self.get_sign(r)
            r.headers['Authorization'] = self.auth_template.format(self.username,
                                self.algorithm, ' '.join(self.headers), sign)

            return r
        except:
            traceback.print_exc()

    def create_date_header(self):
        now = datetime.datetime.utcnow()
        return now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    def get_sign(self, r):
        sign = ''
        for h in self.headers:
            if h == 'request-line':
                sign += '{} {} HTTP/1.1'.format(r.method, r.path_url)
            else:
                sign += '{}: {}'.format(h, r.headers[h.title()])
            sign += '\n'

        h = hmac.new(self.password.encode(self.charset), sign[:-1].encode(self.charset),
                     getattr(hashlib, self.algorithm[5:]))
        return base64.b64encode(h.digest()).decode(self.charset)

    def get_body_digest(self, r):
        # print(r.body)
        if r.body:
            if isinstance(r.body, bytes):
                h = hashlib.sha256(r.body)
            else:
                h = hashlib.sha256(r.body.encode(self.charset))
            return base64.b64encode(h.digest()).decode(self.charset)
        return ''



if __name__ == '__main__':
    resp = requests.post('http://hello.com:8000/',
                         data={"u": "1"},
                         auth=KongHMAC(HMAC_USERNAME, HMAC_SECRET),
                         )
    print(resp.status_code, resp.content)