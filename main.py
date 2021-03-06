
from Weather.weatherInfo import WeatherInfo
from MessageManager.MessageManager import MessageManager
import ModuleCommandChecker
from Bot import Bot
def startMain():
    weatherInfo = WeatherInfo()
    messageManager = MessageManager()
    botclass= Bot.getInstance()
    bot = botclass.bot
    @bot.message_handler(commands=['start', 'weather','time',

                                   '_getinfouser','setmeafk',"seemyafkstatus","deletemyafkstatus",
                                   'wiki','meaning','generatememe','sendmessagebyid',
                                   'totext','chatinfo'])
    def check_commands(message):
        if "/start" in message.text.lower():
            bot.reply_to(message, "Welcome to szBrokenHeart")
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
        elif "/sendmessagebyid" in message.text.lower() or "/sendmessagebyid@szbrokenbot" in message.text.lower():
            search = message.text
            if "/sendmessagebyid@szBrokenBot" in search:
                search = search[search.index("/sendmessagebyid@szBrokenBot") + len("/sendmessagebyid@szBrokenBot"):]
            else:
                search = search[search.index("/sendmessagebyid") + len("/sendmessagebyid"):]
            if len(search) == 0:
                bot.reply_to(message, "Please type id \n/sendmessagebyid id")
            else:
                search = search.split(",")
                i=0
                stringtosend=""
                for x in search:
                    if i >0:
                        stringtosend=stringtosend+x+","
                    i=i+1
                stringtosend= stringtosend.replace("gmeme","generatememe")

                stringtosend = stringtosend[:-1]
                if len(search) == 1:
                    bot.reply_to(message, "Please type text1 and text2 seperated by ,\n/sendmessagebyid text1,text2 ")
                else:
                    messageManager.send_mssagetoGroup(bot, message, search[0] , stringtosend)
        elif "/totext" == message.text.lower() or "/totext@szbrokenbot" == message.text.lower():
            messageManager.send_toText(message, bot)







    @bot.message_handler(func=lambda message: True)
    def messageHandler(message):
        if "_discuss" in message.text.lower():
            messageManager.send_discussion_cheerful(message,bot)
        else:
            messageManager.storeUserToDatabse(message,bot)
            messageManager.checkUserIfHasStatus(message,bot)
            messageManager.checkIfBotMentioned(message,bot)
            ModuleCommandChecker.checkCommand(message)


    # Handles all sent documents and audio files
    @bot.message_handler(content_types=['voice'])
    def handle_docs_audio(message):
        ModuleCommandChecker.checkCommand(message)
    # Handles aimages
    @bot.message_handler(content_types=['photo'])
    def handle_image(message):
        ModuleCommandChecker.checkCommand(message)
    # Handles aimages
    # @bot.message_handler(content_types=['animation'])
    # def handle_image_animation(message):
    #     ModuleCommandChecker.checkCommand(message)

    @bot.callback_query_handler(func=lambda message: True)
    def callBackHandler(call):
        ModuleCommandChecker.checkCallback(call)
        if "Select Your search" == call.message.text:
            messageManager.callBackWikiHandler(call,bot)

    # def subscriptionNextStep_Time(message):
    #     if message.from_user.id in messageManager.userstep:
    #         messageManager.send_subscriptionMessageTime(message,bot)
    #     else:
    #         if message.content_type == 'text':
    #             check_commands(message)
    #         bot.register_next_step_handler_by_chat_id(message.chat.id,subscriptionNextStep_Time)
    def afkNextStep_Message(message):
        if message.from_user.id in messageManager.userstep:
            messageManager.setAfkMessage(message,bot)
        else:
            if message.content_type == 'text':
                check_commands(message)
            bot.register_next_step_handler_by_chat_id(message.chat.id, afkNextStep_Message)


    bot.polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startMain()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
