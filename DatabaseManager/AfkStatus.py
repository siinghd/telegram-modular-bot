import calendar
import time
class AfkStatus:
    def __init__(self,id,message,firstname,createdAt):
        self._id = id
        self._message=message
        self._firstName= firstname
        if createdAt==None:
            self._created_At = self.getTimeStamp()
        else:
            self._created_At = createdAt

    def getTimeStamp(self):
        return calendar.timegm(time.gmtime())