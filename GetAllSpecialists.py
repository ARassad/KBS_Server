from Request import Request


class GetAllSpecialists(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        type_spec = params["type"]

        cursor.execute("SELECT id, [name] FROM Specialist_User WHERE type_specialist={}".format(type_spec))
        specs = cursor.fetchall()

        if specs is not None:
            dataTransferObject.type = type_spec
            dataTransferObject.people = {}
            for s in specs:
                dataTransferObject.people[s[0]] = s[1]

            return

        raise AttributeError
