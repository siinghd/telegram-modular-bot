from DatabaseManager.DatabaseOperation import DatabaseOperation
import soundfile as sf
from pydub import AudioSegment
import speech_recognition as sr
import os
NOTADMIN = "Puff , you are not an admin! get some powers :)"
BOTNOTADMIN = "Puff , I'm not a admin! give me some power to do this! :("
PRIVATECHAT ="Command not avaible in private chat!"
WORNGMSG ="Something went wrong retry!"
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

def toText(bot,fileId,r):
    info = {}
    try:
        file_info = bot.get_file(fileId)
        downloaded_file = bot.download_file(file_info.file_path)
        nameF = file_info.file_unique_id
        nameFogg = nameF + ".ogg"
        with open(nameFogg, 'wb') as new_file:
            new_file.write(downloaded_file)
        file_ogg = AudioSegment.from_ogg(nameFogg)
        filewav = nameF + ".wav"
        file_handle = file_ogg.export(filewav, format="wav")
        nameFwav = nameF + ".wav"
        audio = sr.AudioFile(nameFwav)
        with audio as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)

            res = r.recognize_google(audio ,language="en-IN",show_all=True)

        if len(res) == 0:
            info["status"] = "failed"
            info["message"] = "Check the audio, probably no clear speech found!"
        else:
            stringTosend = "<b>Here is possible text:</b>\n"
            stringTosend = stringTosend + f"""⚫ {res['alternative'][0]['transcript']}\n"""
            info["status"] = "success"
            info["message"] = stringTosend

        if os.path.exists(nameFwav):
            os.remove(nameFwav)
        if os.path.exists(nameFogg):
            os.remove(nameFogg)
        return info

    except Exception as e:
        print(e)
        info["status"] = "failed"
        info["message"] = "Problem in convertion!"
        return info

def getmessageInCommand(message,command,seperator):
    textMessage = message.text
    if command+"@szBrokenBot" in textMessage:
        textMessage = textMessage[textMessage.index(command+"@szBrokenBot") + len(command+"@szBrokenBot"):]
    else:
        textMessage = textMessage[textMessage.index(command) + len(command):]

    textMessage = textMessage.strip()
    if len(textMessage)==0:
         return  ""
    else:
        if seperator is None:
            return  textMessage
        else:
            textMessageParams = textMessage.split(seperator)
            return textMessageParams
