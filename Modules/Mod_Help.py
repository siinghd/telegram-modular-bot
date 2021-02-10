from Modules.Base import Mod_Base
from telebot import types
import ModuleCommandChecker
from Modules.UsefulMethods import getUserIdArray, PRIVATECHAT, getIsAdmin, BOTNOTADMIN, getBotIsAdmin, isPrivateChat, \
    NOTADMIN


class Mod_Help(Mod_Base):
    steps= {}
    def __init__(self):
        super(Mod_Help, self).__init__("Help",["/help"],
                                             ["Help","_Help_Back"])

    def handleOnCommand(self, message, name):
        # try:
            if name == "/help":
                msgHelp = "<b>Time</b> - /time City name\n" + \
                          "<b>Weather</b> - /weather City name\n" + \
                          "<b>Set Afk</b> - /setmeafk Set your status to AFK\n" + \
                          "<b>See if you have afk status</b> - /seemyafkstatus\n" + \
                          "<b>Delete your afk status</b> - /deletemyafkstatus\n" + \
                          "<b>Info from wikipedia</b> - /wiki Word\n" + \
                          "<b>Find meaning</b> - /meaning Word\n" + \
                          "<b>Generate meme (beta)</b> - /generatememe text1,text2\n" + \
                          "<b>Audio to text (beta)</b> - /totext Reply to voice message\n" + \
                          "<b>Text to audio (beta)</b> - /tospeech Reply to text message\n" + \
                          "<b>Modify photo</b> - /modifyphoto Modify your photo to disney style\n"
                self.bot.reply_to(message, msgHelp)
                self.sendHelpMessage(message)
        # except Exception:
        #     print(Exception)

    def sendHelpMessage(self, message):

        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        modNames= ModuleCommandChecker.getActiveModNames()
        try:
            modNames.remove("Mod_Help")
        except:
            pass
        for name in modNames:
            name = name.replace("Mod_","")
            buttons.append(types.InlineKeyboardButton(text=name, callback_data=name))


        markup.add(*buttons)


        markup.row(types.InlineKeyboardButton(text="Add me :)",url = "http://t.me/szBrokenBot?startgroup=true"))
        self.bot.send_message(message.chat.id, "Help", reply_markup=markup)

    def callBackHandler(self, call, name):
            if call.data == "_Help_Back":
                self.bot.delete_message(call.message.chat.id, call.message.id)
                self.sendHelpMessage(call.message)
            else:
                help  = ModuleCommandChecker.getHelpOfModule(call.data)
                self.bot.delete_message(call.message.chat.id,call.message.id)
                markup = types.InlineKeyboardMarkup()
                markup.row(types.InlineKeyboardButton(text="Go back",callback_data="_Help_Back"))
                self.bot.send_message(call.message.chat.id, help, reply_markup=markup)