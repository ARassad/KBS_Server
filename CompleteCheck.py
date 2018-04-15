from Request import Request


class CompleteCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"

        companyId, mark, characteristic, criteria = params["companyId"], params["mark"], params["characteristic"], params["criteria"]

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_current_exam = row[0]

            if criteria in ["goods", "sanitation", "security", "consumerRights"]:

                cursor.execute("UPDATE Examination SET {}={}, about += '{}' WHERE id={}".format(criteria, mark, characteristic, id_current_exam))

                CompleteCheck.__culc_sum_crit(cursor, id_current_exam)

                dataTransferObject.resultRequest = "True"
                return

        raise AttributeError

    @staticmethod
    def __culc_sum_crit(cursor, exam_id):
        cursor.execute("SELECT goods, sanitation, security FROM Examination WHERE id = {}".format(exam_id))
        row = cursor.fetchone()

        if row is not None:
            criteria = [c if c is not None else 0 for c in row]

            sum_crit = sum(criteria) // len(criteria)

            cursor.execute("UPDATE Examination SET consumerRights = {} WHERE id = {}".format(sum_crit, exam_id))

