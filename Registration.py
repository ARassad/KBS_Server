from Request import Request


class RegistrationUser(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select * from ServiceUser where login='{}'".format(params['login']))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("insert into ServiceUser(login, password, type_specialist) values('{}', '{}', {})"
                           .format(params['login'], params['password'], params['type']))
        else:
            dataTransferObject.status = 'Error'
