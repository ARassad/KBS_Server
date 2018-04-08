from Request import Request


class GetBribe(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        company, other, type_other = params["companyId"], params["user"], params["typeUser"]

        def getBribe():
            cursor.execute("SELECT id FROM Bride WHERE id_company={} AND id_grafter={} AND type_grafter={} AND bribe_status='{}'"
                           .format(company, other, type_other, "inProgres"))
            return cursor.fetchone()

        row = getBribe()
        if row is not None:
            dataTransferObject.bribeId = row[0]
            return

        cursor.execute("insert into Bride(id_company, id_grafter, type_grafter, bribe_status) values('{}', {}, {}, '{}')"
                       .format(company, other, type_other, "inProgres"))

        row = getBribe()
        if row is not None:
            dataTransferObject.bribeId = row[0]
            return

        raise AttributeError


class GetAllBribe(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        user, type_user = params["userId"], int(params["typeUser"])

        bribes = None

        if type_user == 2:
            cursor.execute("SELECT id FROM Bride WHERE id_company={} AND bribe_status='{}'".format(user, "inProgres"))
            bribes = cursor.fetchall()
            dataTransferObject.bribes = {}
            for n, b in enumerate(bribes):
                dataTransferObject.bribes[n] = b[0]
            return

        elif type_user == 0 or type_user == 1:
            cursor.execute("SELECT id FROM Bride WHERE id_grafter={} AND bribe_status='{}' AND type_grafter={}"
                           .format(user, "inProgres", type_user))
            bribes = cursor.fetchall()
            dataTransferObject.bribes = {}
            for n, b in enumerate(bribes):
                dataTransferObject.bribes[n] = b[0]
            return

        raise AttributeError


class AgreeToBribe(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        bribeId = int(params["bribeId"])

        cursor.execute("UPDATE Bride SET bribe_status='{}' WHERE id={}".format("completed", bribeId))

        return

