import datetime


class Group:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._timestamp = self.getTimeStamp()

    def getTimeStamp(self):
        return datetime.datetime.now()


