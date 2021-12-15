from Modules.Base import Mod_Base
from Modules.UsefulMethods import isOwner,tryTosendMsg,NOOWNER
import requests
import json
class Mod_Insult(Mod_Base):

    def __init__(self):
        super(Mod_Insult, self).__init__("Insult",["/insult",'/compliment'],
                                             [])

    def handleOnCommand(self, message, name):
        try:
            if name == "/insult":
                self.send_insult(message)
            elif name == '/compliment':
                self.send_compliments(message)

        except Exception as e:
            print(e)


    def send_insult(self,message):
        r = requests.post(
            'https://evilinsult.com/generate_insult.php?lang=en&type=json',
        )
        response = r.text
        dictionary = json.loads(response)
        try:
            if message.reply_to_message is not None:
                tryTosendMsg(message.reply_to_message,dictionary['insult'],self.bot)
            else:
                tryTosendMsg(message,dictionary['insult'],self.bot)

        except Exception as e:
            print(e)

    def send_compliments(self, message):
        r = requests.get(
            'https://complimentr.com/api',
        )
        response = r.text
        dictionary = json.loads(response)
        try:
            if message.reply_to_message is not None:
                tryTosendMsg(message.reply_to_message, dictionary['compliment'], self.bot)
            else:
                tryTosendMsg(message, dictionary['compliment'], self.bot)

        except Exception as e:
            print(e)




