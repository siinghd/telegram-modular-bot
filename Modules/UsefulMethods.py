from DatabaseManager.DatabaseOperation import DatabaseOperation

def getUserIdArray(message,method,cursor):
    arrayOfMentionsId = {}
    metionarray = []
    arrayOfIds = []
    if message.entities != None:
        parsedString = message.text.split(" ")
        for stringM in parsedString:
            if "@" in stringM:
                metionarray.append(stringM)
        for entity in message.entities:
            if entity.type == "text_mention":
                arrayOfMentionsId[entity.user.first_name] =entity.user.id


    if message.reply_to_message != None:
        arrayOfMentionsId[message.reply_to_message.from_user.first_name] =message.reply_to_message.from_user.id
    for mention in arrayOfMentionsId:
        # self.lock.acquire(True)
        arrayOfIds.append(mention)
        # self.lock.release()
    for tagged in metionarray:
        username = tagged[tagged.index("@") + len("@"):]
        # self.lock.acquire(True)
        arrayofid = method(username, cursor)
        # self.lock.release()
        if len(arrayofid) != 0:
            arrayOfMentionsId[username]=arrayofid[0]


    return arrayOfMentionsId
