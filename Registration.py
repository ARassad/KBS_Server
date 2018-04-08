from Request import Request


class RegistrationUser(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.registrationStatus = "Error"

        user_type = int(params["type"])
        login = params["login"]
        password = params["password"]
        name = params["name"]

        cursor.execute("SELECT id FROM LoginInfo WHERE login = '{}'".format(login))
        row = cursor.fetchone()
        if row is not None:
            raise AttributeError

        cursor.execute("insert into LoginInfo(login, password) values('{}', '{}')"
                       .format(login, password))

        cursor.execute("SELECT id FROM LoginInfo WHERE login = '{}'".format(login))
        id_login_info = cursor.fetchone()[0]

        if user_type == 0: # Спеиалист
            client_data = int(params["clientData"])
            cursor.execute("insert into Specialist_User([name], id_login_info, type_specialist) values('{}', {}, {})"
                           .format(name, id_login_info, client_data))
        elif user_type == 1: # Депутат
            cursor.execute("insert into Deputy_User([name], id_login_info) values('{}', '{}')"
                           .format(name, id_login_info))
        elif user_type == 2: # Компания
            client_data = int(params["clientData"])
            cursor.execute("insert into Company_User([name], id_login_info, product_type) values('{}', {}, {})"
                           .format(name, id_login_info, client_data))
        else:
            raise AttributeError

        dataTransferObject.registrationStatus = "Ok"
        return
