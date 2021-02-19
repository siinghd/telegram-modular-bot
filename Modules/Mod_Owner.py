from Modules.Base import Mod_Base
from Modules.UsefulMethods import isOwner,tryTosendMsg,NOOWNER
from DatabaseManager.Group import Group


class Mod_Owner(Mod_Base):
    steps= {}
    def __init__(self):
        super(Mod_Owner, self).__init__("Owner",["/_sg"],
                                             [])

    def handleOnCommand(self, message, name):
        try:
            if isOwner(message):
                if name == "/_sg":
                    self.sendGroups(message)
            else:
                tryTosendMsg(message, NOOWNER, self.bot)
        except Exception as e:
            print(e)

    def sendGroups(self, message):
        resp = self.getGroups()
        if isinstance(resp,str):
            tryTosendMsg(message,resp,self.bot)
        else:
            msg=""
            for group in resp:
                msg+=f"{group._id}  -  {group._name}\n"
            msg += f"Num: {len(resp)}\n"
            tryTosendMsg(message,msg,self.bot)


    def getGroups(self):
        try:
            self.cursor.execute("""Select * from groups""")
            items = self.cursor.fetchall()
            arrayI = []
            for i in items:
                group = Group(i[0],i[1])
                arrayI.append(i[group])

            return arrayI
        except Exception as e:
            print(e)
            return "Something went wrong retry!"



