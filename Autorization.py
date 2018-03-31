from Request import Request


class Autorization(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select * from ServiceUser where login={} and password={}".
                       format(params["login"], params["password"]))
        user = cursor.fetchone()

        if user is not None:
            dataTransferObject.token = "xyz"
        else:
            dataTransferObject.statusAutorization = "ERROR"
