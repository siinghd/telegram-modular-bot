import datetime


def getTimeStamp():
    return datetime.datetime.now()


class Movies:
    def __init__(self, id, name, link, createdat):
        self.id = id
        self.name=name
        self.link= link
        if createdat is None:
            self.created_at = getTimeStamp()
        else:
            self.created_at = createdat

