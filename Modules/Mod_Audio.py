
from Modules.Base import Mod_Base
from Modules.UsefulMethods import getmessageInCommand,isOwner,tryTosendMsg
import os
from gtts import gTTS

class Mod_Audio(Mod_Base):
    user_step=[]
    def __init__(self):
        super(Mod_Audio,self).__init__("Audio",["/tospeech"],
                                        [])

    def handleOnCommand(self,message,name):
        try:
            if name == "/tospeech":
                arguments = getmessageInCommand(message,"/tospeech",",")


                if len(arguments) == 0:
                    tryTosendMsg(message, "Please type the language\n/tospeech language or /tospeech language, text to speech",self.bot)
                elif len(arguments)==1:
                    if message.reply_to_message is None or message.reply_to_message.text is None:
                        tryTosendMsg(message, "Please include a reply voice reply or text to covert!", self.bot)
                    else:
                        self.send_toSpeech(message.id, message.reply_to_message.text, arguments[0],message.chat.id)
                elif len(arguments)==2:
                    if message.reply_to_message is not None and  message.reply_to_message.text is not None:
                        self.send_toSpeech(message.id, message.reply_to_message.text, arguments[0],message.chat.id)
                    self.send_toSpeech(message.id, arguments[1], arguments[0],message.chat.id)
                elif len(arguments)==3:
                    if isOwner(message):
                        self.send_toSpeech(message.id, arguments[1], arguments[0], int(arguments[2]))

        except Exception as e:
            print(e)

    def send_toSpeech(self, messageid,texttospecch,lang,chatid):
        try:
            # Language in which you want to convert
            lang=lang.strip()
            language = lang[0:2]
            stringid= messageid
            string_mp=str(stringid)+ ".ogg"
            # Passing the text and language to the engine,
            # here we have marked slow=False. Which tells
            # the module that the converted audio should
            # have a high speed
            myobj = gTTS(text=texttospecch, lang=language, slow=False)
            # string_ogg = str(stringid)+".ogg"
            # Saving the converted audio in a mp3 file named
            # welcome
            myobj.save(string_mp)
            # file_mp = AudioSegment.from_mp3(string_mp)
            # file_handle = file_mp.export(string_ogg, format="ogg")
            # sendVoice
            voice = open(string_mp, 'rb')
            self.bot.send_voice(chatid, voice)
            if os.path.exists(string_mp):
                os.remove(string_mp)

        except:
            self.bot.send_message(chatid, "Problem in convertion, probably problem with language you insert!")
    def help_mod(self):
        help_string =f"Help of {self.mod_name}\n"+\
              f"/tospeech - text to speech\n"

        return help_string