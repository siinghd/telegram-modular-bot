import json
import random
from telebot import types
from datetime import datetime
from DatabaseManager.DatabaseOperation import DatabaseOperation
from DatabaseManager.DatabaseInitialization import DatabaseInitiaization
from DatabaseManager.Group import Group
from DatabaseManager.User import User
from DatabaseManager.AfkStatus import AfkStatus
from MemeManager.ImgFlip import ImgFlip
import wikipedia
import wolframalpha
from threading import Lock
import csv
from PyDictionary import PyDictionary
import speech_recognition as sr
import os
from gtts import gTTS
import requests
from Modules import UsefulMethods
class MessageManager:
    userstep = []
    userData = [None, None, None]
    databaseOp = DatabaseOperation()
    databaseInitiaization = DatabaseInitiaization.getInstance()
    conn = databaseInitiaization.getConnection()
    cursor = conn.cursor()
    lock = Lock()
    imgFlip = ImgFlip()
    dictionary = PyDictionary()
    app_id = 'QRH4VG-AVUXR7LKYJ'  # get your own at https://products.wolframalpha.com/api/
    client = wolframalpha.Client(app_id)
    r = sr.Recognizer()

    def __init__(self):
        self.cursor.execute("""
            create table if not exists users
            (
                id  integer primary key,
                is_bot  integer not null,
                first_name  text not null,
                username  text not null,
                last_name  text not null,
                created_At timestamp not null
            );
            """)
        self.conn.commit()
        self.cursor.execute("""create table if not exists afkstatus
(
    userId  integer primary key,
    message  text not null,
    created_At timestamp not null,
    FOREIGN KEY(userId) REFERENCES users(id)
);""")
        self.conn.commit()

    def send_weather(self, weatherInfo, bot, message, location):
        try:
            weatherinfo = weatherInfo.getWeatherInfo(location, None)
            bot.reply_to(message, weatherinfo)
        except Exception:
            pass

    def send_discussion_cheerful(self, message, bot):
        array = ["⚫ It is considered mannerless to interrupt someone while talking. "
                 "Everyone has a say and one should respect and let your turn come for you to have your say. "
                 "There could be a situation where you may need to cut short the speaker, if so then do it politely "
                 "with due respect and apologize for doing ",
                 "⚫ Always remember that it is a discussion and not a battle."
                 "In the heat of the moment never lose your control of speech and decency. "
                 "You are there to share your point of view and not to start an argument. "
                 "Respect others views and do not try to dominate your views or point. "
                 "Being patient and calm is the key.",
                 "⚫ Your confidence is seen in your eyes. "
                 "Hence maintain eye contact with the evaluator while initiating the discussion. "
                 "Later share eye contacts with your peers in a consistent manner. "
                 "During the session avoid looking at the evaluator and concentrate on the peers.\n"
                 "Even when you are listening to the opposition candidate, make sure you are slightly "
                 "turned towards the angle where the candidate is present and use gestures such as "
                 "nodding in appreciation in between the presentation.",
                 "⚫ Carry on with the discussion Guys 😊 "
                 "hope you have a peaceful and polite discussion on the topic 😊"]
        parsedString = message.text.split(" ")
        metionarray = []
        stringMessage = random.choice(array)
        i = 0
        try:
            for stringM in parsedString:
                if "@" in stringM:
                    metionarray.append(stringM)
            for entity in message.entities:
                if entity.type == "text_mention":
                    stringMessage = stringMessage + " <a href='tg://user?id={id}'>{name}</a>".format(id=entity.user.id,
                                                                                                     name=entity.user.first_name)
                elif entity.type == "mention":
                    stringMessage = stringMessage + " " + metionarray[i]
                    i = i + 1
            bot.reply_to(message, stringMessage)
        except Exception:
            pass

    def send_time(self, weatherInfo, bot, message, location):
        try:
            weatherinfo = weatherInfo.getTime(location, None)
            bot.reply_to(message, weatherinfo)
        except Exception:
            pass


    # def getUserStep(self, messageId):
    #     for x in self.userstep:
    #         if x == messageId:
    #             return 1
    #
    #     return 0

    def storeUserToDatabse(self, message, bot):
        if message.from_user.is_bot == False:
            bot=0
        else:
            bot=1
        if message.from_user.username ==None:
            username ="None"
        else:
            username = message.from_user.username
        if message.from_user.last_name == None:
            lastname= "None"
        else:
            lastname = message.from_user.last_name
        user = User(message.from_user.id,bot,message.from_user.first_name
                    ,username,lastname)
        group=None
        if message.chat.type == "group" or message.chat.type == "supergroup":
            group = Group(message.chat.id,message.chat.title)
        try:
            if group!=None:
                self.databaseOp.insertGroup(group,self.cursor)
            # self.lock.acquire(True)
            self.databaseOp.insertUser(user,self.cursor)
            self.conn.commit()
            # self.lock.release()
        except:
            pass

    def sendUserInfoFile(self, message, bot):

        arrayTitle=["id","is_bot_1_is_bot","first_name","username","last_name"]
        try:
            users = self.databaseOp.getUserInfo(self.cursor)

            try:
                with open('users.csv', 'w',encoding='utf-8',newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(arrayTitle)
                    for user in users:
                        arrayBody = [user._id,user._is_bot,user._first_name,user._username,user._last_name]
                        writer.writerow(arrayBody)

                doc = open('users.csv', 'rb')
                bot.send_document(message.chat.id,doc)
            except Exception:
                pass
        except Exception:
            pass

    def send_userAfkMessage(self, message, bot):
        markup = types.ForceReply(selective=True)
        self.userstep.append(message.from_user.id)
        sent = bot.reply_to(message, "Please type Your AFK Message :", reply_markup=markup)
        self.userData[2] = sent.message_id
    def setAfkMessage(self, message, bot):
        bot.delete_message(message.chat.id,self.userData[2])
        afkuser=AfkStatus(message.from_user.id,message.text.replace("'",""),None,None)
        string = self.databaseOp.insertStatus(afkuser,self.cursor)
        self.conn.commit()
        if string=="ok":
            bot.reply_to(message,"Your afk status has been set correctly!")
        else:
            bot.reply_to(message, string)

    def send_afkStatus(self, message, bot):
        array = self.databaseOp.getUserStatusByID(message.from_user.id, self.cursor)

        if len(array)==0:
            bot.reply_to(message,"You don't have any status set!")
        else:

            for x in array:
                dt_object = datetime.fromisoformat(str(x._created_At))
                dt_object = dt_object.strftime("%m/%d/%Y, %H:%M")
                msgSend = "<b>On : {date}</b>\nYour message:\n".format(date=dt_object)+\
                          "<code>{message}</code>".format(message=x._message)
                bot.reply_to(message,msgSend)

    def send_deleteMyAFK(self, message, bot):
        msg = self.databaseOp.deleteStatus(message.from_user.id, self.cursor)
        self.conn.commit()
        bot.reply_to(message,msg)

    def checkUserIfHasStatus(self, message, bot):
        stringMentions = ""
        arrayOfMentionsId=[]
        metionarray = []
        if message.entities!=None:
            parsedString = message.text.split(" ")
            for stringM in parsedString:
                if "@" in stringM:
                    metionarray.append(stringM)
            for entity in message.entities:
                if entity.type == "text_mention":
                    arrayOfMentionsId.append(entity.user.id)



        if message.reply_to_message!=None:
            arrayOfMentionsId.append(message.reply_to_message.from_user.id)
        messageTosend=""
        for mention in arrayOfMentionsId:
            # self.lock.acquire(True)
            array = self.databaseOp.getUserStatusByID(mention,self.cursor)
            messageTosend=self.addMessageToTheStringStatus(array,messageTosend)
            # self.lock.release()
        for tagged in metionarray:
            username= tagged[tagged.index("@")+len("@"):]
            # self.lock.acquire(True)
            arrayofid = self.databaseOp.getUserByUsername(username,self.cursor)
            # self.lock.release()
            if len(arrayofid)!=0:
                # self.lock.acquire(True)
                arrayOfafkstatus = self.databaseOp.getUserStatusByID(arrayofid[0], self.cursor)
                # self.lock.release()
                messageTosend = self.addMessageToTheStringStatus(arrayOfafkstatus, messageTosend)

        if len(messageTosend)!=0:
            bot.reply_to(message,messageTosend)

    def addMessageToTheStringStatus(self,array,string):
        string=""
        if not isinstance(array, str):
            if len(array) != 0:
                dt_object = datetime.fromisoformat(str(array[0]._created_At))
                d = dt_object.strftime("%m/%d/%Y, %H:%M")
                string = string + "<b >User </b>: <a href='tg://user?id={id}'>{name}</a> is AFK!\n".format(
                    id=array[0]._id,
                    name=array[0]._firstName) + \
                                "<b>Message from him/her</b> :<code> {message}</code>\n".format(message=array[0]._message)+\
                        "<b>At </b>: {time}\n------------------\n".format(time=d)
            return string
        else:
            return string

    def send_wikisearch(self, bot, message, search):
        self.userstep.append(message.from_user.id)
        try:
            search_Result = wikipedia.search(search,results = 5, suggestion = True)
            markup = types.InlineKeyboardMarkup()
            buttons = []
            for result in search_Result[0]:
                buttons.append(types.InlineKeyboardButton(text=result, callback_data=result))

            buttons.append(types.InlineKeyboardButton(text="Cancel", callback_data="Cancel"))
            for button in buttons:
                markup.row(button)

            bot.send_message(message.chat.id, "Select Your search", reply_markup=markup)
        except Exception:
            bot.reply_to(message, "Something went wrong retry!")



    def callBackWikiHandler(self, call, bot):
        if call.from_user.id in self.userstep:
            self.userstep.remove(call.from_user.id)
            if "Cancel" in call.data:
                bot.delete_message(call.message.chat.id, call.message.id)
            else:
                try:
                    search_Result = wikipedia.page(call.data)

                    string = "<b>{title}</b>\n".format(title=search_Result.title)+\
                            "{content}\n".format(content=search_Result.summary)+\
                            "<a href='{link}'>Read More</a>".format(link=search_Result.url)
                    bot.delete_message(call.message.chat.id, call.message.id)
                    bot.send_message(call.message.chat.id,string)
                except wikipedia.exceptions.PageError :
                    bot.send_message(call.message.chat.id, "Something went wrong retry!\nProbably the page got removed or doesn't exist in english!")
                except wikipedia.exceptions.DisambiguationError:
                    bot.send_message(call.message.chat.id, "Something went wrong retry!\nProbably the word choosen have multple reference\nSorry can't help you")

    def send_meaning(self, bot, message, word):

        try:
            dic = self.dictionary.meaning(word)
            msgToSend = ""
            for key in dic:
                i = 1
                msgToSend=msgToSend+f"<b>{key}</b>\n"
                for x in dic[key]:
                     msgToSend = msgToSend + f"<b>{i}</b> - <code>{x}</code>\n\n"
                     i=i+1
            bot.reply_to(message,msgToSend)
        except :
            bot.reply_to(message,f"Something went wrong retry!\nProbably there is no word {word} matching!")

    def send_Meme(self, bot, message, param, param1):
        images = self.imgFlip.getMeme("https://api.imgflip.com/get_memes")
        image = random.choice(images)
        resp = self.imgFlip.generateMeme(param,param1,image['id'])
        if resp['success'] == False:
            bot.reply_to(message,"Something went wrong retry!")
        else:
            bot.reply_to(message,resp['data']['url'])

    def send_mssagetoGroup(self, bot, message, param, param1):
        bot.send_message(int(param),param1);

    def checkIfBotMentioned(self, message, bot):
        found = False
        if message.reply_to_message !=None:
            if message.reply_to_message.from_user.id == 1496422338:
                found=True
        elif "@szBrokenBot" in message.text:
            found = True

        if found==True:
            query = message.text.replace("@szBrokenBot","")
            msgtoSend="<b>Info</b>\n"
            try:
                res = self.client.query(query)
                if res.success =="true":
                    if "solve" in query or  "Solve" in query:
                        for pod in res.pods:
                            for sub in pod.subpods:
                                msgtoSend=msgtoSend+f"<b>{pod.title}</b>\n\n{sub.plaintext}\n"
                    else:
                        for pod in res.pods:
                            for sub in pod.subpods:
                                    msgtoSend=msgtoSend+f"<b>{pod.title}</b>\n\n{sub.plaintext}\n"

                    bot.reply_to(message,msgtoSend)
                else:
                    pass
                    # bot.reply_to(message, "Ops something went wrong , don't ask me advanced questions! I'm in early stage :(")
            except:
                 pass


    def send_toText(self, message, bot):

        if message.reply_to_message==None or message.reply_to_message.voice==None:
            bot.reply_to(message,"Please include a reply voice reply!")
        else:
            resp = UsefulMethods.toText(bot,message.reply_to_message.voice.file_id,self.r)
            bot.reply_to(message,resp["message"])


    def send_toSpeech(self, message, bot,lang):
        if message.reply_to_message==None or message.reply_to_message.text==None:
            bot.reply_to(message,"Please include a reply voice reply!")
        else:
            try:
                # Language in which you want to convert
                lang=lang.strip()
                language = lang[0:2]
                stringid= message.reply_to_message.message_id
                string_mp=str(stringid)+ ".ogg"
                # Passing the text and language to the engine,
                # here we have marked slow=False. Which tells
                # the module that the converted audio should
                # have a high speed
                myobj = gTTS(text=message.reply_to_message.text, lang=language, slow=False)
                # string_ogg = str(stringid)+".ogg"
                # Saving the converted audio in a mp3 file named
                # welcome
                myobj.save(string_mp)
                # file_mp = AudioSegment.from_mp3(string_mp)
                # file_handle = file_mp.export(string_ogg, format="ogg")
                # sendVoice
                voice = open(string_mp, 'rb')
                bot.send_voice(message.chat.id, voice)
                if os.path.exists(string_mp):
                    os.remove(string_mp)

            except:
                bot.send_message(message.chat.id, "Problem in convertion, probably problem with language you insert!")

    def getIsAdmin(self,bot,message):
        isAdmin = False
        for member in bot.get_chat_administrators(message.chat.id):
            if member.user.id == message.from_user.id:
                isAdmin = True
                break
        return isAdmin



