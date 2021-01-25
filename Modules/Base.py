from DatabaseManager.DatabaseInitialization import DatabaseInitiaization
from Bot import Bot

class Mod_Base:
    botClass= Bot.getInstance()
    def __init__(self,name,callBackHandlerName):
        self.databaseInitiaization = DatabaseInitiaization.getInstance()
        self.conn = self.databaseInitiaization.getConnection()
        self.cursor = self.conn.cursor()
        self.mod_name = name
        self.mod_call_handler_name = callBackHandlerName
        self.bot = self.botClass.bot
