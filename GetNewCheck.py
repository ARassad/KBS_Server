from Request import Request


class GetNewCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        specId = params["specialistId"]

        dataTransferObject.isCheckExist = "False"
        dataTransferObject.companyId = ""
        dataTransferObject.companyName = ""

        cursor.execute("SELECT id, [name] FROM Company_User WHERE id_current_exam IN (SELECT id FROM Examination WHERE id_duma_specialist = {id} OR id_doctor = {id} OR id_policeman = {id})"
                       .format(id=specId))
        row = cursor.fetchone()

        if row is not None:
            dataTransferObject.isCheckExist = "True"

            dataTransferObject.companyId = row[0]
            dataTransferObject.companyName = row[1]
