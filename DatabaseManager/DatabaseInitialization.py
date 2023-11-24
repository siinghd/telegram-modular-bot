import psycopg2
class DatabaseInitiaization:
    databaseName=""
    user=""
    password=""
    host=""
    __instance = None
    def __init__(self):
        if DatabaseInitiaization.__instance == None:
            DatabaseInitiaization.__instance = self
        self._conn = psycopg2.connect(database=self.databaseName, user=self.user, password=self.password, host=self.host, port="5432")

    def getConnection(self):
       return self._conn
    def closeConnection(self):
        self._conn.close()

    @staticmethod
    def getInstance():
        if DatabaseInitiaization.__instance == None:
            DatabaseInitiaization()
        return DatabaseInitiaization.__instance
