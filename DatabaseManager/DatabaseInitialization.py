import sqlite3
class DatabaseInitiaization:
    def __init__(self,databaseName):
        self._conn = sqlite3.connect(databaseName,check_same_thread=False)
    def getConnection(self):
       return self._conn
    def closeConnection(self):
        self._conn.close()

