from Request import Request


class GetInterlocutors(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        userId, user_type = params["userId"], int(params["userType"])

        if user_type == 2:
            dataTransferObject.interlocutors = GetInterlocutors.__get_for_company(cursor, userId)

        elif user_type == 0:
            dataTransferObject.interlocutors = GetInterlocutors.__get_for_Specialist(cursor, userId)

        elif user_type == 1:
            dataTransferObject.interlocutors = GetInterlocutors.__get_for_deputy(cursor, userId)

        else:
            raise AttributeError

        return

    @staticmethod
    def __get_for_deputy(cursor, dep):

        cursor.execute(
            "SELECT id, [name] FROM Company_User WHERE Company_User.id_current_exam IN (SELECT id FROM Examination WHERE id_deputy = {} )".format(dep))
        companys = cursor.fetchall()

        res = {}
        if companys is not None:
            for c in companys:
                res[c[0]] = c[1]

        return res

    @staticmethod
    def __get_for_Specialist(cursor, spec_id):

        cursor.execute("SELECT id, [name] FROM Company_User WHERE Company_User.id_current_exam IN (SELECT id FROM Examination WHERE {} IN (id_duma_specialist, id_doctor, id_policeman) )".format(spec_id))
        companys = cursor.fetchall()

        res = {}
        if companys is not None:
            for c in companys:
                res[c[0]] = c[1]

        return res

    @staticmethod
    def __get_for_company(cursor, company_id):

        cursor.execute("SELECT id_current_exam FROM Company_User WHERE id = {}".format(company_id))
        row = cursor.fetchone()

        if row is not None:
            id_exam = row[0]

            cursor.execute("SELECT id_deputy, id_duma_specialist, id_doctor, id_policeman FROM Examination WHERE id = {}".format(id_exam))
            specs = cursor.fetchone()

            if specs is not None:

                res = {}

                cursor.execute("SELECT id, [name] FROM Deputy_User WHERE id = {}".format(specs[0]))
                dep = cursor.fetchone()

                res[str(dep[0]) + str(".0")] = dep[1]

                cursor.execute("SELECT id, [name] FROM Specialist_User WHERE id IN ({}, {}, {}) ".format(specs[1], specs[2], specs[3]))
                specials = cursor.fetchall()

                for s in specials:
                    res[str(s[0])] = s[1]

                return res

        raise AttributeError


