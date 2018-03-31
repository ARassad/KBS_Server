from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qsl, urlsplit
from cgi import parse_header
from cgi import parse_multipart
from urllib.parse import parse_qs
import json
from Request import DataTransferObject
from Autorization import Autorization

"""
    КАК СДЕЛАТЬ ЗАПРОС
    Наследуемся от Request и перегружаем request
    
    class TestReq(Request):
        @staticmethod
        def request(cursor, params, dataTransferObject):
            dataTransferObject.result = "HELLO"
    
    также можно перегрузить verification_params для проверки параметров на корректность
    
    потом вставить получившееся обьект класса в соотвествующий словарь 
    api_methods_get["TestReq"] = TestReq()
"""

api_methods_get, api_methods_post = {}, {}


api_methods_post["Autorization"] = Autorization()


class HttpServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        url = self.requestline[9:-9]
        dct = dict(parse_qsl(urlsplit(url).path))
        if dct.get('id', None) is not None:
            dct['id'] = int(dct['id'])

        mymethod = dct.get('method', None)
        if mymethod is not None and api_methods_get.get(mymethod) is not None:
            value = api_methods_get[mymethod](dct)
            self.wfile.write(str.encode(value))
            print(value)
        else:
            print("method cannot parse (None value)")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        postvars = self.parse_POST()
        for key, val in postvars.items():
            mstr = key + val[0]
        dct = json.loads(mstr)

        mymethod = self.requestline[10:-9]

        if mymethod is not None and api_methods_post.get(mymethod) is not None:
            value = api_methods_post[mymethod](dct)
            self.wfile.write(str.encode(value))
            print(value)
        else:
            print("method cannot parse (None value)")

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            s = self.rfile.read(length)
            s = s.decode()
            postvars = parse_qs(
                s,
                keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def error_request(self, message):
        obj = DataTransferObject()
        obj.status = "Error"
        obj.message = message
        self.wfile.write(str.encode(obj.toJSON()))


def run_httpserver(server_class=HTTPServer, handler_class=HttpServer, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Start')
    httpd.serve_forever()


if __name__ == "__main__":
    run_httpserver()

