from Modules.Base import Mod_Base
from DatabaseManager.DatabaseOperation import DatabaseOperation
from DatabaseManager.Group import Group
from DatabaseManager.NewsSubscription import NewsSubscription
import time
from datetime import datetime
import json
from FeedReceiver.feedReceiver import FeedReceiver
import random
from telebot import types
from Modules.UsefulMethods import getIsAdmin
import ModuleCommandChecker
from threading import Thread
class Mod_News(Mod_Base):
    dbop = DatabaseOperation()
    fr = FeedReceiver()
    userstep = []
    userData = [None, None, None]
    def __init__(self):
        super(Mod_News, self).__init__(["/currentnews",'/subscribenews',
                                        '/unsubscribenews','/listnewssubscriptions'],
                                       ["Select time","Cancel Subscription"])
        thread = Thread(target=self.send_newsFrequently, args=())
        thread.start()

    def handleOnCommand(self,message,name):
        if name=="/currentnews":
            country = message.text
            if "/currentnews@szBrokenBot" in country:
                country = country[country.index("/currentnews@szBrokenBot") + len("/currentnews@szBrokenBot"):]
            else:
                country = country[country.index("/currentnews") + len("/currentnews"):]
            if len(country) == 0:
                self.bot.reply_to(message, "Please type country\n/news country name")
            else:
                self.send_news(self.fr,message, message.chat.id, country.strip())
        elif name=="/subscribenews":

            if message.chat.type =="group" or message.chat.type=="supergroup":
                if getIsAdmin(self.bot,message):
                    self.send_subscriptionMessageCity(message)
                    self.bot.register_next_step_handler_by_chat_id(message.chat.id, self.subscriptionNextStep_Time)

                else:
                    self.bot.reply_to(message,"You are not admin in this group")
            else:
                self.send_subscriptionMessageCity(message)
                self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.subscriptionNextStep_Time)
        elif name == "/unsubscribenews" :
            self.send_unSubscriptionNews(message)
        elif name == "/listnewssubscriptions" :
            self.listNewsSubscriptions(message)

    def callBackHandler(self,call,name):
        if "Select time" == name:
            self.callBackNewsHandler(call)
        if "Cancel Subscription" == name:
            self.callBackCancelNewsHandler(call)

    def send_news(self, fr, message, chatId, country):
        link = "https://news.google.com/news/rss/headlines/section/geo/"
        try:
            fr.check_feeds(link + country)
            entries = fr.get_feeds()
            json_object = json.dumps(entries, indent=4)
            resp = json.loads(json_object)
            if message is None:
                self.bot.send_message(chatId, "<b>Here are    last 5 news</b>")
            else:
                self.bot.reply_to(message, "<b>Here are last 5 news</b>")
            for x in random.sample(resp, k=5):
                string = "\n<a href='" + x["link"] + "'><b>" + x['title'] + "</b></a>\n"
                self.bot.send_message(chatId, string)
        except Exception:
            self.bot.send_message(chatId, "Something bad happened Can't send news")


    def send_subscriptionMessageCity(self, message):
        self.userData[0] = message.chat.id
        markup = types.ForceReply(selective=True)
        self.userstep.append(message.from_user.id)
        sent = self.bot.reply_to(message, "Please type Country name :", reply_markup=markup)
        self.userData[2] = sent.message_id

    def subscriptionNextStep_Time(self,message):

        if message.from_user.id in self.userstep:
            self.send_subscriptionMessageTime(message)
        else:
            if message.content_type == 'text':
                ModuleCommandChecker.checkCommand(message)

            self.bot.register_next_step_handler_by_chat_id(message.chat.id,self.subscriptionNextStep_Time)

    def send_subscriptionMessageTime(self, message):
        self.bot.delete_message(self.userData[0], self.userData[2])
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

        self.bot.send_message(message.chat.id, "Select time", reply_markup=markup)


    def callBackNewsHandler(self, data):
        if data.from_user.id in self.userstep:
            self.userstep.remove(data.from_user.id)
            if "Cancel" in data.data:
                self.bot.delete_message(self.userData[0], data.message.id)
            else:
                group = Group(data.message.chat.id, data.message.chat.title)
                newsSubscription = NewsSubscription(data.message.id, self.userData[1], data.data, self.userData[0], 1)
                resp = self.dbop.insertGroup(group, self.cursor)
                if resp == "ok":
                    self.conn.commit()
                    stringMsg = self.dbop.insertnewSubscription(newsSubscription, self.cursor)
                    self.conn.commit()
                    self.bot.delete_message(self.userData[0], data.message.id)
                    self.bot.send_message(self.userData[0], stringMsg)
                else:
                    self.bot.send_message(self.userData[0], "Ops something went wrong!")

    def send_unSubscriptionNews(self, message):
        self.userstep.append(message.from_user.id)
        activeSubs = self.dbop.getNews_byGroupSubscriptions(self.cursor, message.chat.id)
        if len(activeSubs) == 0:
            self.bot.reply_to(message, "This chat has 0 subscriptions to cancel")
            return
        markup = types.InlineKeyboardMarkup()
        buttons = []
        for activeSub in activeSubs:
            buttons.append(types.InlineKeyboardButton(text="Cancel " + activeSub._state, callback_data=activeSub._id))

        buttons.append(types.InlineKeyboardButton(text="Cancel", callback_data="Cancel"))
        for b in buttons:
            markup.row(b)

        self.bot.send_message(message.chat.id, "Cancel Subscription", reply_markup=markup)

    def callBackCancelNewsHandler(self, call):
        if call.from_user.id in self.userstep:
            self.userstep.remove(call.from_user.id)
            if "Cancel" in call.data:
                self.bot.delete_message(call.message.chat.id, call.message.id)
            else:
                msg = self.dbop.update_subscription(call.data, None, 0, self.cursor)
                self.conn.commit()
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.bot.send_message(call.message.chat.id, msg)
    def listNewsSubscriptions(self, message):
        activeSubs = self.dbop.getNews_byGroupSubscriptions(self.cursor, message.chat.id)
        if len(activeSubs) == 0:
            self.bot.reply_to(message, "This chat has 0 news subscriptions ")
            return

        string = "<b>Here is Your list :</b>\n"
        for activeSub in activeSubs:
            string = string + "{state} at {time}\n".format(state=activeSub._state, time=activeSub._time)

        self.bot.reply_to(message, string)

    def send_newsFrequently(self):
        for days in range(0, 365):
            for hours in (0, 24):
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if current_time > "12:00":
                    current_time = now.strftime("%I:%M") + "PM"
                else:
                    current_time = now.strftime("%I:%M") + "AM"
                items = self.dbop.getNews_Subscriptions(self.cursor)
                if not isinstance(items, str):
                    for item in items:
                        if current_time == item._time:
                            self.send_news(self.fr, None, item._groupId, item._state)
                            time.sleep(15)
                time.sleep(60)
