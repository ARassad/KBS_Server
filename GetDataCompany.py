from Request import Request


class GetDataCompany(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("SELECT * FROM Company_User WHERE id = {}".format(params["id"]))
        row = cursor.fetchone()

        if row is not None:
            dataTransferObject.name = row[2]
            dataTransferObject.productType = row[3]

            return

        raise AttributeError
