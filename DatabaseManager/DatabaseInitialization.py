import psycopg2
class DatabaseInitiaization:
    databaseName="d53u103lovkkna"
    user="vxoxttfardbovf"
    password="aedd150942e9b21c9ae78bdd01140c6148a72839060ce4bab047ee46012e0e4f"
    host="ec2-52-205-145-201.compute-1.amazonaws.com"
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
