from Request import Request


class GetNewCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        specId = params["specialistId"]

        dataTransferObject.isCheckExist = "False"
        dataTransferObject.companyId = ""
        dataTransferObject.companyName = ""
        
        cursor.execute("SELECT type_specialist FROM Specialist_User WHERE id = {}".format(specId))
        t = cursor.fetchone()[0]

        types = ["id_doctor", "id_policeman", "id_duma_specialist"]

        cursor.execute("SELECT Company_User.id, [name], X.id FROM Company_User INNER JOIN (SELECT id FROM Examination WHERE {type} = {id} AND status='inProgres') X ON id_current_exam = X.id"
                       .format(id=specId, type = types[t]))
        company = cursor.fetchone()

        if company is not None:
            cursor.execute("SELECT type_specialist FROM Specialist_User WHERE id = {}".format(specId))
            type = cursor.fetchone()[0]

            type_crit = ["goods", "security", "sanitation"]

            cursor.execute("SELECT {} FROM Examination WHERE {} = {} AND id = {} ".format(type_crit[type], types[type], specId, company[2]))
            row = cursor.fetchone()
            if row is not None and row[0] is not None:
                return

        if company is not None:
            dataTransferObject.isCheckExist = "True"

            dataTransferObject.companyId = company[0]
            dataTransferObject.companyName = company[1]
