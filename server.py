from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qsl, urlsplit
from cgi import parse_header
from cgi import parse_multipart
from urllib.parse import parse_qs
import json
from Request import DataTransferObject
from Autorization import Autorization
from Registration import RegistrationUser
from Bribe import GetBribe, GetAllBribe, AgreeToBribe, ChangeSumBribe, GetDataBribe
from GetDataCompany import GetDataCompany
from GetDataSpecialist import GetDataSpecialist
from GetDataDeputy import GetDataDeputy
from GetCompanyCheckData import GetCompanyCheckData
from CancelCheck import CancelCheck
from ConfirmCheck import ConfirmCheck
from RejectCheck import RejectCheck
from CompleteCheck import CompleteCheck
from CreateCheck import CreateCheck
from GetAllSpecialists import GetAllSpecialists
from GetInterlocutors import GetInterlocutors
from GetNewCheck import GetNewCheck
from GetCheckInProgress import GetCheckInProgress
from GetCheckCompleted import GetCheckCompleted
from GetCompanyCheckDataInProgres import GetCompanyCheckDataInProgres

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
api_methods_post["signUp"] = RegistrationUser()
api_methods_post["signIn"] = Autorization()

api_methods_get["getCompanyCheckDataInProgres"] = GetCompanyCheckDataInProgres()
api_methods_get["getChecksCompleted"] = GetCheckCompleted()
api_methods_get["getChecksInProgress"] = GetCheckInProgress()
api_methods_get["getNewCheck"] = GetNewCheck()
api_methods_get["getInterlocutors"] = GetInterlocutors()
api_methods_get["getAllSpecialists"] = GetAllSpecialists()
api_methods_get["createCheck"] = CreateCheck()
api_methods_get["completeCheck"] = CompleteCheck()
api_methods_get["rejectCheck"] = RejectCheck()
api_methods_get["confirmCheck"] = ConfirmCheck()
api_methods_get["cancelCheck"] = CancelCheck()
api_methods_get["getCompanyCheckData"] = GetCompanyCheckData()
api_methods_get["getDataBribe"] = GetDataBribe()
api_methods_get["changeSumBribe"] = ChangeSumBribe()
api_methods_get["agreeToBribe"] = AgreeToBribe()
api_methods_get["getBribe"] = GetBribe()
api_methods_get["getAllBribe"] = GetAllBribe()
api_methods_get["getDataCompany"] = GetDataCompany()
api_methods_get["getDataSpecialist"] = GetDataSpecialist()
api_methods_get["getDataDeputy"] = GetDataDeputy()


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
        param = {}
        for key, val in postvars.items():
            mstr = key + val[0]
            param[key] = val[0]
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

