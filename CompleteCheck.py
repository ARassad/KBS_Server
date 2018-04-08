from Request import Request


class CompleteCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"

        companyId, mark, characteristic = params["companyId"], params["mark"], params["characteristic"]

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_current_exam = row[0]

            if characteristic in ["goods", "sanitation", "security", "consumerRights"]:

                cursor.execute("UPDATE Examination SET {}={} WHERE id={}".format(characteristic, mark, id_current_exam))

                dataTransferObject.resultRequest = "True"
                return

        raise AttributeError
