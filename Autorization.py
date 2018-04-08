from Request import Request


class Autorization(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.loginStatus = "Error"

        cursor.execute("select id from LoginInfo where login='{}' and password='{}'".
                       format(params["login"], params["password"]))
        user_auth = cursor.fetchone()

        if user_auth is None:
            raise AttributeError
        id_login_info = user_auth[0]

        types_spec = ["Specialist_User", "Deputy_User", "Company_User"]
        for type in range(len(types_spec)):

            cursor.execute("SELECT id FROM {} WHERE id_login_info = {}".format(types_spec[type], id_login_info))
            row = cursor.fetchone()

            if row is not None:
                id_ = row[0]
                dataTransferObject.userId = id_
                dataTransferObject.type = type
                dataTransferObject.loginStatus = "Ok"
                return

        raise AttributeError
