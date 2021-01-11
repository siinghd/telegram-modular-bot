import psycopg2
class DatabaseInitiaization:
    def __init__(self,databaseName,user,password,host):
        self._conn = psycopg2.connect(database=databaseName, user=user, password=password, host=host, port="5432")

    def getConnection(self):
       return self._conn
    def closeConnection(self):
        self._conn.close()

