from Request import Request


class GetDataSpecialist(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("SELECT * FROM Specialist_User WHERE id = {}".format(params["id"]))
        row = cursor.fetchone()

        if row is not None:
            dataTransferObject.name = row[1]
            dataTransferObject.type = row[3]

            return

        raise AttributeError