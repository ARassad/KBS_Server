from Request import Request


class CreateCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"

        companyId, deputyId, doctorId, policeId, doomId = params["companyId"], params["deputyId"], params["doctorId"], params["policeId"], params["doomId"]

        cursor.execute("INSERT INTO Examination(id_company, id_deputy, id_duma_specialist, id_doctor, id_policeman, status) VALUES ({}, {}, {}, {}, {}, '{}')"
                                        .format(companyId, deputyId, doomId, doctorId, policeId, "inProgres"))

        dataTransferObject.resultRequest = "True"

        return

