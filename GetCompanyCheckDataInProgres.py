from Request import Request


class GetCompanyCheckDataInProgres(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        companyId = int(params["companyId"])

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(companyId))
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            id_exam = row[0]

            cursor.execute("SELECT goods, sanitation, security, consumerRights, about FROM Examination WHERE id = {}"
                           .format(id_exam))
            exam = cursor.fetchone()

            if exam is not None:
                dataTransferObject.goods = exam[0]
                dataTransferObject.sanitation = exam[1]
                dataTransferObject.security = exam[2]
                dataTransferObject.consumerRights = exam[3]

                dataTransferObject.characteristic = exam[4]

                return

        raise AttributeError