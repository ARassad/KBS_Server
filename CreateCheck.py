from Request import Request


class CreateCheck(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.resultRequest = "False"

        companyId, deputyId, doctorId, policeId, doomId = params["companyId"], params["deputyId"], params["doctorId"], params["policeId"], params["doomId"]

        cursor.execute("INSERT INTO Examination(id_company, id_deputy, id_duma_specialist, id_doctor, id_policeman, status) OUTPUT INSERTED.id VALUES ({}, {}, {}, {}, {}, '{}')"
                        .format(companyId, deputyId, doomId, doctorId, policeId, "inProgres"))

        row = cursor.fetchone()

        if row is not None:
            last_exam_id = row[0]

            cursor.execute("UPDATE Company_User SET id_current_exam = {} WHERE id = {}".format(last_exam_id, companyId))

            dataTransferObject.resultRequest = "True"

        return
