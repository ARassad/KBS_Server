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


class GetLastMessage(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        from_, to = params["fromUser"], params["toUser"]
        dataTransferObject.message = GetLastMessage.messages.getLastMessage(from_, to)
