from Request import Request


class GetDataDeputy(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("SELECT [name] FROM Deputy_User WHERE id = {}".format(params["id"]))
        row = cursor.fetchone()

        if row is not None:
            dataTransferObject.name = row[0]
            dataTransferObject.companies = {}

            cursor.execute("SELECT id, name FROM Company_User")
            rows = cursor.fetchall()

            if rows is not None:
                for comp in rows:
                    dataTransferObject.companies[comp[0]] = comp[1]

            return

        raise AttributeError
