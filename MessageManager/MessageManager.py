import json
import time
import random
from telebot import types
from datetime import datetime
from DatabaseManager.DatabaseOperation import DatabaseOperation
from DatabaseManager.DatabaseInitialization import DatabaseInitiaization
from DatabaseManager.Group import Group
from DatabaseManager.NewsSubscription import NewsSubscription
from DatabaseManager.User import User
from DatabaseManager.AfkStatus import AfkStatus
from MemeManager.ImgFlip import ImgFlip
import wikipedia
from threading import Lock
import csv
from PyDictionary import PyDictionary



class MessageManager:
    userstep = []
    userData = [None, None, None]
    databaseOp = DatabaseOperation()
    databaseInitiaization = DatabaseInitiaization("telegramDb.db")
    conn = databaseInitiaization.getConnection()
    cursor = conn.cursor()
    lock = Lock()
    imgFlip = ImgFlip()
    dictionary = PyDictionary()
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
    def send_news(self, fr, bot, message, chatId, country):
        link = "https://news.google.com/news/rss/headlines/section/geo/"
        try:
            fr.check_feeds(link + country)
            entries = fr.get_feeds()
            json_object = json.dumps(entries, indent=4)
            resp = json.loads(json_object)
            if message is None:
                bot.send_message(chatId, "<b>Here are    last 5 news</b>")
            else:
                bot.reply_to(message, "<b>Here are last 5 news</b>")
            for x in random.sample(resp, k=5):
                string = "\n<a href='" + x["link"] + "'><b>" + x['title'] + "</b></a>\n"
                bot.send_message(chatId, string)
        except Exception:
            bot.send_message(chatId, "Something bad happened Can't send news")

    def send_alisha_msg(self, message, bot):
        try:
            sent = bot.reply_to(message, "Ab bas kar alisha!!")
            xarray = ["❤", "💛", "💚", "💜"]
            i = 0
            for x in range(0, 15):
                if (i == 4):
                    i = 0

                else:
                    bot.edit_message_text(xarray[i], message.chat.id, sent.message_id)
                    i = i + 1
                    time.sleep(3)
        except Exception:
            pass

    def send_aliora_brother(self, message, bot):
        try:
            sent = bot.reply_to(message, "❤💛💚💜💖")

            bot.edit_message_text("❤💛💚💖💜", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("❤💛💖💜💚", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("❤💖💜💚💛", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("💖💜💚💛❤", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("💖💜💚❤💛", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("💖💜❤💛💚", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("💖❤💛💚💜", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("❤💛💚💜💖", message.chat.id, sent.message_id)
        except Exception:
            pass

    def send_copr_brother(self, message, bot):
        try:
            sent = bot.reply_to(message, "<b>THIS IS</b>")
            bot.edit_message_text("<b>THIS IS C</b>", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("<b>THIS IS CO</b>", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("<b>THIS IS COR</b>", message.chat.id, sent.message_id)
            time.sleep(2)
            bot.edit_message_text("<b>THIS IS CORP</b>", message.chat.id, sent.message_id)
        except Exception:
            pass

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
        i = 0;
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

    def send_subscriptionMessageTime(self, message, bot):
        bot.delete_message(self.userData[0], self.userData[2])
        self.userData[1] = message.text
        markup = types.InlineKeyboardMarkup()
        buttons = []
        buttons.append(types.InlineKeyboardButton(text="12:00AM", callback_data="12:00AM"))
        buttons.append(types.InlineKeyboardButton(text="01:00AM", callback_data="01:00AM"))
        buttons.append(types.InlineKeyboardButton(text="02:00AM", callback_data="02:00AM"))
        buttons.append(types.InlineKeyboardButton(text="03:00AM", callback_data="03:00AM"))
        buttons.append(types.InlineKeyboardButton(text="04:00AM", callback_data="04:00AM"))
        buttons.append(types.InlineKeyboardButton(text="05:00AM", callback_data="05:00AM"))
        buttons.append(types.InlineKeyboardButton(text="06:00AM", callback_data="06:00AM"))
        buttons.append(types.InlineKeyboardButton(text="07:00AM", callback_data="07:00AM"))
        buttons.append(types.InlineKeyboardButton(text="08:00AM", callback_data="08:00AM"))
        buttons.append(types.InlineKeyboardButton(text="09:00AM", callback_data="09:00AM"))
        buttons.append(types.InlineKeyboardButton(text="10:00AM", callback_data="10:00AM"))
        buttons.append(types.InlineKeyboardButton(text="11:00AM", callback_data="11:00AM"))
        buttons.append(types.InlineKeyboardButton(text="12:00PM", callback_data="12:00PM"))
        buttons.append(types.InlineKeyboardButton(text="01:00PM", callback_data="01:00PM"))
        buttons.append(types.InlineKeyboardButton(text="02:00PM", callback_data="02:00PM"))
        buttons.append(types.InlineKeyboardButton(text="03:00PM", callback_data="03:00PM"))
        buttons.append(types.InlineKeyboardButton(text="04:00PM", callback_data="04:00PM"))
        buttons.append(types.InlineKeyboardButton(text="05:00PM", callback_data="05:00PM"))
        buttons.append(types.InlineKeyboardButton(text="06:00PM", callback_data="06:00PM"))
        buttons.append(types.InlineKeyboardButton(text="07:00PM", callback_data="07:00PM"))
        buttons.append(types.InlineKeyboardButton(text="08:00PM", callback_data="08:00PM"))
        buttons.append(types.InlineKeyboardButton(text="09:00PM", callback_data="09:00PM"))
        buttons.append(types.InlineKeyboardButton(text="10:00PM", callback_data="10:00PM"))
        buttons.append(types.InlineKeyboardButton(text="11:00PM", callback_data="11:00PM"))
        buttons.append(types.InlineKeyboardButton(text="Cancel", callback_data="Cancel"))
        markup.row(buttons[0], buttons[1], buttons[2])
        markup.row(buttons[3], buttons[4], buttons[5])
        markup.row(buttons[6], buttons[7], buttons[8])
        markup.row(buttons[9], buttons[10], buttons[11])
        markup.row(buttons[12], buttons[13], buttons[14])
        markup.row(buttons[15], buttons[16], buttons[17])
        markup.row(buttons[18], buttons[19], buttons[20])
        markup.row(buttons[21], buttons[22], buttons[23])
        markup.row(buttons[24])

        bot.send_message(message.chat.id, "Select time", reply_markup=markup)

    def send_subscriptionMessageCity(self, message, bot):
        self.userData[0] = message.chat.id
        markup = types.ForceReply(selective=True)
        self.userstep.append(message.from_user.id)
        sent = bot.reply_to(message, "Please type Country name :", reply_markup=markup)
        self.userData[2] = sent.message_id

    # def getUserStep(self, messageId):
    #     for x in self.userstep:
    #         if x == messageId:
    #             return 1
    #
    #     return 0

    def callBackNewsHandler(self, data, bot):
        if data.from_user.id in self.userstep:
            self.userstep.remove(data.from_user.id)
            if "Cancel" in data.data:
                bot.delete_message(self.userData[0], data.message.id)
            else:
                group = Group(data.message.chat.id, data.message.chat.title)
                newsSubscription = NewsSubscription(data.message.id, self.userData[1], data.data, self.userData[0], 1)
                resp = self.databaseOp.insertGroup(group, self.cursor)
                if resp == "ok":
                    self.conn.commit()
                    stringMsg = self.databaseOp.insertnewSubscription(newsSubscription, self.cursor)
                    self.conn.commit()
                    bot.delete_message(self.userData[0], data.message.id)
                    bot.send_message(self.userData[0], stringMsg)
                else:
                    bot.send_message(self.userData[0], "Ops something went wrong!")

    def send_newsFrequently(self, fr, bot):

        for days in range(0, 365):
            for hours in (0, 24):
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if current_time > "12:00":
                    current_time = now.strftime("%I:%M") + "PM"
                else:
                    current_time = now.strftime("%I:%M") + "AM"
                items = self.databaseOp.getNews_Subscriptions(self.cursor)

                for item in items:
                    if current_time == item._time:
                        self.send_news(fr, bot, None, item._groupId, item._state)
                        time.sleep(15)

                time.sleep(60)

    def send_unSubscriptionNews(self, message, bot):
        self.userstep.append(message.from_user.id)
        activeSubs = self.databaseOp.getNews_byGroupSubscriptions(self.cursor, message.chat.id)
        if len(activeSubs) == 0:
            bot.reply_to(message, "This chat has 0 subscriptions to cancel")
            return
        markup = types.InlineKeyboardMarkup()
        buttons = []
        for activeSub in activeSubs:
            buttons.append(types.InlineKeyboardButton(text="Cancel " + activeSub._state, callback_data=activeSub._id))

        buttons.append(types.InlineKeyboardButton(text="Cancel", callback_data="Cancel"))
        for b in buttons:
            markup.row(b)

        bot.send_message(message.chat.id, "Cancel Subscription", reply_markup=markup)

    def callBackCancelNewsHandler(self, call, bot):
        if call.from_user.id in self.userstep:
            self.userstep.remove(call.from_user.id)
            if "Cancel" in call.data:
                bot.delete_message(call.message.chat.id, call.message.id)
            else:
                msg = self.databaseOp.update_subscription(call.data, None, 0, self.cursor)
                self.conn.commit()
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, msg)

    def listNewsSubscriptions(self, message, bot):
        activeSubs = self.databaseOp.getNews_byGroupSubscriptions(self.cursor, message.chat.id)
        if len(activeSubs) == 0:
            bot.reply_to(message, "This chat has 0 news subscriptions ")
            return

        string = "<b>Here is Your list :</b>\n"
        for activeSub in activeSubs:
            string = string + "{state} at {time}\n".format(state=activeSub._state, time=activeSub._time)

        bot.reply_to(message, string)

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
        try:
            self.lock.acquire(True)
            self.databaseOp.insertUser(user,self.cursor)
            self.conn.commit()
            self.lock.release()
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
        afkuser=AfkStatus(message.from_user.id,message.text,None,None)
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
                dt_object = datetime.fromtimestamp(x._created_At)
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
                    stringMentions = stringMentions + " <a href='tg://user?id={id}'>{name}</a>".format(
                        id=entity.user.id,
                        name=entity.user.first_name)


        if message.reply_to_message!=None:
            arrayOfMentionsId.append(message.reply_to_message.from_user.id)
        messageTosend=""
        for mention in arrayOfMentionsId:
            self.lock.acquire(True)
            array = self.databaseOp.getUserStatusByID(mention,self.cursor)
            messageTosend=self.addMessageToTheStringStatus(array,messageTosend)
            self.lock.release()
        for tagged in metionarray:
            username= tagged[tagged.index("@")+len("@"):]
            self.lock.acquire(True)
            arrayofid = self.databaseOp.getUserByUsername(username,self.cursor)
            self.lock.release()
            if len(arrayofid)!=0:
                self.lock.acquire(True)
                arrayOfafkstatus = self.databaseOp.getUserStatusByID(arrayofid[0], self.cursor)
                self.lock.release()
                messageTosend = self.addMessageToTheStringStatus(arrayOfafkstatus, messageTosend)

        if len(messageTosend)!=0:
            bot.reply_to(message,messageTosend)

    def addMessageToTheStringStatus(self,array,string):
        if len(array) != 0:
            date_time = datetime.fromtimestamp(array[0]._created_At)
            d = date_time.strftime("%m/%d/%Y, %H:%M")
            string = string + "<b>User </b>: <a href='tg://user?id={id}'>{name}</a> is AFK!\n".format(
                id=array[0]._id,
                name=array[0]._firstName) + \
                            "<b>Message from him/her</b> :<code> {message}</code>\n".format(message=array[0]._message)+\
                    "<b>At </b>: {time}\n------------------\n".format(time=d)
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
