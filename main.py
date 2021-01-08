import telebot
from FeedReceiver.feedReceiver import FeedReceiver
from Weather.weatherInfo import WeatherInfo
from MessageManager.MessageManager import MessageManager
from threading import Thread
def startMain():
    bot = telebot.TeleBot("1496422338:AAHagrAf4xuDUydPeV7aUpUDTIpeJd37qpA", parse_mode="HTML")
    fr = FeedReceiver()
    weatherInfo = WeatherInfo()
    messageManager = MessageManager()
    thread = Thread(target=messageManager.send_newsFrequently, args=(fr,bot))
    thread.start()

    @bot.message_handler(commands=['start', 'help', 'currentnews', 'weather','time',
                                   'subscribenews','unsubscribenews' ,'listnewssubscriptions',
                                   '_getinfouser','setmeafk',"seemyafkstatus","deletemyafkstatus",
                                   'wiki','meaning','generatememe'])
    def check_commands(message):
        if "/start" in message.text.lower():
            bot.reply_to(message, "Welcome to szBrokenHeart")
        elif "/help" in message.text.lower():
            msgHelp = "<b>Subscribenews</b> - /subscribenews to daily news update\n"+ \
                      "<b>UnSubscribenews</b> - /unsubscribenews Cancel your subscriptions\n" + \
                      "<b>List news subscriptions</b> - /listnewssubscriptions list news subscriptions\n" + \
                      "<b>Time</b> - /time City name\n"+\
                      "<b>Weather</b> - /weather City name\n"+\
                      "<b>Set Afk</b> - /setmeafk Set your status to AFK\n"+\
                      "<b>See if you have afk status</b> - /seemyafkstatus\n"+\
                      "<b>Delete your afk status</b> - /deletemyafkstatus\n"+ \
                      "<b>Info from wikipedia</b> - /wiki Word\n"+ \
                      "<b>Find meaning</b> - /meaning Word\n"+ \
                      "<b>Generate meme (beta)</b> - /generatememe text1,text2\n"
            bot.reply_to(message, msgHelp)
        elif "/currentnews" in message.text.lower():
             country = message.text
             if "/currentnews@szBrokenBot" in country:
                 country = country[country.index("/currentnews@szBrokenBot") + len("/currentnews@szBrokenBot"):]
             else:
                 country = country[country.index("/currentnews") + len("/currentnews"):]
             if len(country)==0:
                 bot.reply_to(message,"Please type country\n/news country name")
             else:
                messageManager.send_news(fr,bot,message,message.chat.id,country.strip())
        elif "/weather" in message.text.lower():
            city = message.text
            if "/weather@szBrokenBot" in city:
                city = city[city.index("/weather@szBrokenBot") + len("/weather@szBrokenBot"):]
            else:
                city = city[city.index("/weather") + len("/weather"):]
            if len(city) == 0:
                bot.reply_to(message, "Please type City name\n/weather city name")
            else:
                messageManager.send_weather(weatherInfo,bot,message,city)
        elif "/meaning" in message.text.lower():
            word = message.text
            if "/meaning@szBrokenBot" in word:
                word = word[word.index("/meaning@szBrokenBot") + len("/meaning@szBrokenBot"):]
            else:
                word = word[word.index("/meaning") + len("/meaning"):]
            if len(word) == 0:
                bot.reply_to(message, "Please type Word name\n/meaning word")
            else:
                messageManager.send_meaning(bot,message,word)
        elif "/time" in message.text.lower():
            city = message.text
            if "/time@szBrokenBot" in city:
                city = city[city.index("/time@szBrokenBot") + len("/time@szBrokenBot"):]
            else:
                city = city[city.index("/time") + len("/time"):]
            if len(city) == 0:
                bot.reply_to(message, "Please type City name\n/time city name")
            else:
                messageManager.send_time(weatherInfo,bot,message,city)
        elif "/wiki" in message.text.lower():
            search = message.text
            if "/wiki@szBrokenBot" in search:
                search = search[search.index("/wiki@szBrokenBot") + len("/wiki@szBrokenBot"):]
            else:
                search = search[search.index("/wiki") + len("/wiki"):]
            if len(search) == 0:
                bot.reply_to(message, "Please type word to search\n/wiki word")
            else:
                messageManager.send_wikisearch(bot,message,search)
        elif "/_getinfouser" == message.text.lower() or "/_getinfouser@szbrokenbot" == message.text.lower():
            messageManager.sendUserInfoFile(message,bot)

        elif "/subscribenews" == message.text.lower() or "/subscribenews@szbrokenbot" == message.text.lower():
            messageManager.send_subscriptionMessageCity(message,bot)
            bot.register_next_step_handler_by_chat_id(message.chat.id,subscriptionNextStep_Time)
        elif "/unsubscribenews" == message.text.lower() or "/unsubscribenews@szbrokenbot" == message.text.lower():
            messageManager.send_unSubscriptionNews(message, bot)

        elif "/listnewssubscriptions" == message.text.lower() or "/listnewssubscriptions@szbrokenbot" == message.text.lower():
            messageManager.listNewsSubscriptions(message, bot)
        elif "/setmeafk" == message.text.lower() or "/setmeafk@szbrokenbot" == message.text.lower():
            messageManager.send_userAfkMessage(message,bot)
            bot.register_next_step_handler_by_chat_id(message.chat.id,afkNextStep_Message)
        elif "/seemyafkstatus" == message.text.lower() or "/seemyafkstatus@szbrokenbot" == message.text.lower():
            messageManager.send_afkStatus(message,bot)
        elif "/deletemyafkstatus" == message.text.lower() or "/deletemyafkstatus@szbrokenbot" == message.text.lower():
            messageManager.send_deleteMyAFK(message,bot)
        elif "/generatememe" in message.text.lower() or "/generatememe@szbrokenbot" in message.text.lower():
            stringtext = message.text
            if "/generatememe@szBrokenBot" in stringtext:
                stringtext = stringtext[stringtext.index("/generatememe@szBrokenBot") + len("/generatememe@szBrokenBot"):]
            else:
                stringtext = stringtext[stringtext.index("/generatememe") + len("/generatememe"):]

            if len(stringtext) == 0:
                bot.reply_to(message, "Please type text1 and text2 seperated by ,\n/generatememe text1,text2 ")
            else:
                stringtexts = stringtext.split(",")
                if len(stringtexts) == 1:
                    bot.reply_to(message, "Please type text1 and text2 seperated by ,\n/generatememe text1,text2 ")
                else:
                    messageManager.send_Meme(bot, message, stringtexts[0] , stringtexts[1])



    @bot.message_handler(func=lambda message: True)
    def messageHandler(message):
        if "alisha cutie" in message.text.lower():
            messageManager.send_alisha_msg(message,bot)
        elif "aliora brother" in message.text.lower():
            messageManager.send_aliora_brother(message,bot)
        elif "corp brother" in message.text.lower():
            messageManager.send_copr_brother(message,bot)
        elif "_discuss" in message.text.lower():
            messageManager.send_discussion_cheerful(message,bot)
        else:
            messageManager.storeUserToDatabse(message,bot)
            messageManager.checkUserIfHasStatus(message,bot)


    @bot.callback_query_handler(func=lambda message: True)
    def callBackHandler(call):
        if "Select time" == call.message.text:
            messageManager.callBackNewsHandler(call,bot)
        if "Cancel Subscription" == call.message.text:
            messageManager.callBackCancelNewsHandler(call,bot)
        if "Select Your search" == call.message.text:
            messageManager.callBackWikiHandler(call,bot)

    def subscriptionNextStep_Time(message):
        if message.from_user.id in messageManager.userstep:
            messageManager.send_subscriptionMessageTime(message,bot)
        else:
            check_commands(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id,subscriptionNextStep_Time)
    def afkNextStep_Message(message):
        if message.from_user.id in messageManager.userstep:
            messageManager.setAfkMessage(message,bot)
        else:
            check_commands(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id, afkNextStep_Message)



    bot.polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startMain()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
