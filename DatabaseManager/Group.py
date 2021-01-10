import calendar
import time


class Group:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._timestamp = self.getTimeStamp()

    def getTimeStamp(self):
        return calendar.timegm(time.gmtime())


