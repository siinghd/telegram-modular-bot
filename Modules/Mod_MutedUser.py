from Modules.Base import Mod_Base
from DatabaseManager.MutedUser import MutedUser
from DatabaseManager.DatabaseOperation import DatabaseOperation
from Modules.UsefulMethods import getUserIdArray , getIsAdmin ,NOTADMIN
from threading import Thread
class Mod_MutedUser(Mod_Base):
    dbop = DatabaseOperation()

    def __init__(self):
        super(Mod_MutedUser,self).__init__(["fmute","funmute"])

    def handleOnCommand(self,bot,message,name):
        if name == "fmute":
            if getIsAdmin(bot,message):
                reason = message.text
                if "/fmute@szBrokenBot" in reason:
                    reason = reason[reason.index("/fmute@szBrokenBot") + len("/fmute@szBrokenBot"):]
                else:
                    reason = reason[reason.index("/fmute") + len("/fmute"):]

                userIds = getUserIdArray(message,self.dbop.getUserByUsername,self.cursor)
                for id in userIds:
                    mutedUser = MutedUser(userIds[id],None,None)
                    self.insertMutedUser(mutedUser)
                    bot.reply_to(message, f"User : {id} set to force mute!")
            else:
                bot.reply_to(message,NOTADMIN)

        elif name =="funmute":
            if getIsAdmin(bot, message):
                userIds = getUserIdArray(message, self.dbop.getUserByUsername, self.cursor)
                for id in userIds:
                    mutedUser = MutedUser(userIds[id], None, None)
                    res=self.deleteMutedUser(mutedUser)
                    bot.reply_to(message,res)
            else:
                bot.reply_to(message,NOTADMIN)

    def getEveryMessageMethod(self,message,bot):
        user = self.getMutedUserById(message.from_user.id)
        if len(user)>0:
            try:
                bot.delete_message(message.chat.id,message.id)
            except:
                pass


    def insertMutedUser(self,mutedUser):
        try:
            self.cursor.execute(f"""Select userid from mutedusers where userid={mutedUser._id}""")
            item = self.cursor.fetchall();
            if len(item)==0:
                self.cursor.execute(f"INSERT INTO mutedusers VALUES ({mutedUser._id},'{mutedUser._reason}','{mutedUser._created_At}')")

            return "ok"
        except Exception:
            return "Something went wrong retry!"

    def getMutedUserById(self,id):
        try:
            self.cursor.execute(f"""Select * from mutedusers WHERE userId={id}""")
            items = self.cursor.fetchall()
            arrayI = []
            for i in items:
                x = MutedUser(i[0], i[1], i[2])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def deleteMutedUser(self,mutedUser):
        try:
            self.cursor.execute(f"""Select userId from mutedusers where userId={mutedUser._id}""")
            item = self.cursor.fetchall()
            if len(item)==0:
                return "User is already unmuted"

            else:
                self.cursor.execute(f"""DELETE FROM mutedusers
            WHERE userId={mutedUser._id}""")
                return "User unmuted seccessfully"
        except Exception:
            return "Something went wrong retry!"



