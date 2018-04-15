from Request import Request


class ConfirmCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"
        companyId = int(params["companyId"])

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_current_exam = row[0]

            cursor.execute(" SET ANSI_NULLS OFF SELECT * FROM Examination WHERE id={} AND goods != null AND sanitation != null AND security != null AND consumerRights != null".format(id_current_exam))
            row = cursor.fetchone()

            if row is not None:
                cursor.execute("UPDATE Examination SET status ='{}' WHERE id = {}".format("confirmed", id_current_exam))

                cursor.execute("UPDATE Company_User SET id_last_exam={}, id_current_exam=null WHERE id = {}".format(id_current_exam, companyId))

                dataTransferObject.resultRequest = "True"

                return

        raise AttributeError
