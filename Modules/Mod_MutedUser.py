from Modules.Base import Mod_Base
from DatabaseManager.MutedUser import MutedUser
from DatabaseManager.DatabaseOperation import DatabaseOperation
from Modules.UsefulMethods import getUserIdArray,tryTosendMsg ,PRIVATECHAT,getIsAdmin,BOTNOTADMIN ,getBotIsAdmin,isPrivateChat,NOTADMIN ,isOwner
class Mod_MutedUser(Mod_Base):
    dbop = DatabaseOperation()

    def __init__(self):
        super(Mod_MutedUser,self).__init__("MutedUser",["/fmute","/funmute"],[])

    def handleOnCommand(self,message,name):
        try:
            if not isPrivateChat(message):
                if name == "/fmute":
                        if getBotIsAdmin(self.bot,message):
                            if isOwner(message) or getIsAdmin(self.bot,message):

                                reason = message.text
                                if "/fmute@szBrokenBot" in reason:
                                    reason = reason[reason.index("/fmute@szBrokenBot") + len("/fmute@szBrokenBot"):]
                                else:
                                    reason = reason[reason.index("/fmute") + len("/fmute"):]

                                userIds = getUserIdArray(message,self.dbop.getUserByUsername,self.cursor)
                                for id in userIds:
                                    mutedUser = MutedUser(userIds[id],None,None,message.chat.id)
                                    self.insertMutedUser(mutedUser)
                                    self.bot.send_message(message.chat.id, f"User : {id} set to force mute!")
                            else:
                                tryTosendMsg(message,NOTADMIN,self.bot)

                        else:
                            tryTosendMsg(message, BOTNOTADMIN, self.bot)


                elif name =="/funmute":
                    if getBotIsAdmin(self.bot,message):
                        if isOwner(message) or getIsAdmin(self.bot, message):
                            userIds = getUserIdArray(message, self.dbop.getUserByUsername, self.cursor)
                            for id in userIds:
                                mutedUser = MutedUser(userIds[id], None, None,message.chat.id)
                                res=self.deleteMutedUser(mutedUser)
                                self.bot.send_message(message.chat.id,res)
                        else:
                            tryTosendMsg(message, NOTADMIN, self.bot)

                    else:
                        tryTosendMsg(message, BOTNOTADMIN, self.bot)

            else:
                tryTosendMsg(message, PRIVATECHAT, self.bot)

        except Exception:
            print(Exception)

    def getEveryMessageMethod(self,message):
        mutedUser = MutedUser(message.from_user.id, None, None, message.chat.id)
        user = self.getMutedUserById(mutedUser)
        if len(user)>0:
            try:
                self.bot.delete_message(message.chat.id,message.id)
            except:
                pass


    def insertMutedUser(self,mutedUser):

        try:
            self.cursor.execute(f"""Select userid from mutedusers where userid={mutedUser._id} AND groupid = {mutedUser._groupid}""")
            item = self.cursor.fetchall()
            if len(item)==0:
                self.cursor.execute(f"INSERT INTO mutedusers VALUES ({mutedUser._id},'{mutedUser._reason}','{mutedUser._created_At}',{mutedUser._groupid})")

            return "ok"
        except Exception:
            return "Something went wrong retry!"

    def getMutedUserById(self,mutedUser):
        try:
            self.cursor.execute(f"""Select * from mutedusers WHERE userId={mutedUser._id} AND groupid={mutedUser._groupid}""")
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
            self.cursor.execute(f"""Select userId from mutedusers where userId={mutedUser._id} AND groupid={mutedUser._groupid}""")
            item = self.cursor.fetchall()
            if len(item)==0:
                return "User is already unmuted"

            else:
                self.cursor.execute(f"""DELETE FROM mutedusers
            WHERE userId={mutedUser._id} AND groupid={mutedUser._groupid}""")
                return "User unmuted successfully"
        except Exception:
            return "Something went wrong retry!"


    def help_mod(self):
        help_string =f"Help of MutedUser\n"+\
              f"/fmute - set user to force mute(used also with admins!)\n"+\
              f"/funmute - remove user from force mute"
        return help_string
