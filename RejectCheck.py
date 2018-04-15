from Request import Request


class RejectCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"

        companyId = int(params["companyId"])

        cursor.execute("SELECT id_last_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_current_exam = row[0]

            cursor.execute("UPDATE Examination SET goods=null, sanitation=null, security=null, consumerRights=null, status ='{}' WHERE id = {}".format("inProgres", id_current_exam))

            #cursor.execute("UPDATE Company_User SET id_current_exam={}, id_last_exam=null WHERE id = {}".format(id_current_exam, companyId))

            dataTransferObject.resultRequest = "True"
            return

        raise AttributeError
