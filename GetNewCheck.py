from Request import Request


class GetNewCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        specId = params["specialistId"]

        dataTransferObject.isCheckExist = "False"
        dataTransferObject.companyId = ""
        dataTransferObject.companyName = ""

        cursor.execute("SELECT id, [name] FROM Company_User WHERE id_current_exam IN (SELECT id FROM Examination WHERE id_duma_specialist = {id} OR id_doctor = {id} OR id_policeman = {id} AND status='inProgres')"
                       .format(id=specId))
        company = cursor.fetchone()

        if company is not None:
            cursor.execute("SELECT type_specialist FROM Specialist_User WHERE id = {}".format(specId))
            type = cursor.fetchone()[0]

            types = ["id_doctor", "id_policeman", "id_duma_specialist"]
            type_crit = ["goods", "security", "sanitation"]

            cursor.execute("SELECT {} FROM Examination WHERE {} = {} AND id_company = {} ".format(type_crit[type], types[type], specId, company[0]))
            row = cursor.fetchone()
            if row is not None and row[0] is not None:
                return

        if company is not None:
            dataTransferObject.isCheckExist = "True"

            dataTransferObject.companyId = company[0]
            dataTransferObject.companyName = company[1]
