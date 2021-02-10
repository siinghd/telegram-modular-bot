from DatabaseManager.DatabaseOperation import DatabaseOperation


NOTADMIN = "Puff , you are not an admin! get some powers :)"
BOTNOTADMIN = "Puff , I'm not a admin! give me some power to do this! :("
PRIVATECHAT ="Command not avaible in private chat!"
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

def getIsAdmin(bot,message):
    isAdmin = False
    for member in bot.get_chat_administrators(message.chat.id):
        if member.user.id == message.from_user.id:
            isAdmin = True
            break
    return isAdmin

def getBotIsAdmin(bot,message):
    isAdmin = False
    botId= bot.get_me()

    botId=botId.id
    for member in bot.get_chat_administrators(message.chat.id):
        if member.user.id == botId:
            isAdmin = True
            break
    return isAdmin
def isPrivateChat(message):
    if message.chat.type == "group" or message.chat.type == "supergroup" :
        return False
    else:
        return True

