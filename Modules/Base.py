from DatabaseManager.DatabaseInitialization import getDatabaseInitiaization
class Mod_Base:
    def __init__(self,name,callBackHandlerName):
        self.databaseInitiaization = getDatabaseInitiaization()
        self.conn = self.databaseInitiaization.getConnection()
        self.cursor = self.conn.cursor()
        self.mod_name = name
        self.mod_call_handler_name = callBackHandlerName
