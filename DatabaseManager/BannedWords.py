import datetime
class BannedWords:
    def __init__(self,id,groupid,word,createdAt):
        self._id = id
        self._groupid = groupid
        self._word=word
        if createdAt==None:
            self._created_At = self.getTimeStamp()
        else:
            self._created_At = createdAt

    def getTimeStamp(self):
        return datetime.datetime.now()