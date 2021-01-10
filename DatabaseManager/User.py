import calendar
import time
class User:
    def __init__(self,id,is_bot,first_name,username,last_name):
        self._id = id
        self._is_bot = is_bot
        self._first_name = first_name
        self._username = username
        self._last_name = last_name
        self._created_At = self.getTimeStamp()

    def getTimeStamp(self):
        return calendar.timegm(time.gmtime())