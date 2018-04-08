from Request import Request


class CancelCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        companyId = int(params["companyId"])

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_current_exam = row[0]

            cursor.execute("UPDATE Company_User SET id_current_exam={} WHERE id = {}".format("null", companyId))

            cursor.execute("UPDATE Examination SET status ='{}' WHERE id = {}".format("canceled", id_current_exam))

            return

        raise AttributeError