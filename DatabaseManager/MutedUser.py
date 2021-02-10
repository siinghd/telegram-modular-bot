import datetime
class MutedUser:
    def __init__(self,id,reason,createdAt,groupid):
        self._id = id
        self._reason=reason
        if createdAt==None:
            self._created_At = self.getTimeStamp()
        else:
            self._created_At = createdAt
        self._groupid=groupid

    def getTimeStamp(self):
        return datetime.datetime.now()