from Request import Request


class GetCheckInProgress(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):

        cursor.execute("SET ANSI_NULLS OFF SELECT id, [name] FROM Company_User WHERE id_current_exam IN (SELECT id FROM Examination WHERE goods=null OR sanitation=null OR security=null OR consumerRights = null)")
        row = cursor.fetchall()

        if row is not None:
            dataTransferObject.companies = {}

            for c in row:
                dataTransferObject.companies[c[0]] = c[1]
