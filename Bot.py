import telebot
class Bot:
    bot = None
    __instance=None
    def __init__(self):
        if Bot.__instance == None:
            Bot.__instance = self
        self.bot = telebot.TeleBot("1496422338:AAHagrAf4xuDUydPeV7aUpUDTIpeJd37qpA", parse_mode="HTML")

    @staticmethod
    def getInstance():
        if Bot.__instance == None:
            Bot()
        return Bot.__instance
