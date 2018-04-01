from Request import Request

class Storage:
    """
    
    """
    def __init__(self):
        self.storage = {} #  {(from, to):[messages]}

    def sendMessage(self, from_, to, mes):
        if self.storage.get((from_, to)) is not None:
            self.storage[(from_, to)] = [mes]
        else:
            self.storage[(from_, to)].append(mes)

    def getLastMessage(self, from_, to):
        if self.storage.get((from_, to)) is not None:
            return self.storage.get((from_, to))[-1]
        return None


STOR = Storage()


class SendMessage(Request):
    messages = STOR

    @staticmethod
    def request(cursor, params, dataTransferObject):
        from_, to, mes = params["fromUser"], params["toUser"], params["message"]
        messages.sendMessage(from_, to, mes)


class GetLastMessage(Request):
    messages = STOR

    @staticmethod
    def request(cursor, params, dataTransferObject):
        from_, to = params["fromUser"], params["toUser"]
        dataTransferObject.message = messages.getLastMessage(from_, to)
