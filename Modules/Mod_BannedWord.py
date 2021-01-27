from Modules.Base import Mod_Base
from DatabaseManager.BannedWords import BannedWords
from Modules.UsefulMethods import getUserIdArray , getIsAdmin ,NOTADMIN
class Mod_BannedWord(Mod_Base):
    def __init__(self):
        super(Mod_BannedWord, self).__init__(["/bword","/listbword","/dbword"],
                                       [])
    def handleOnCommand(self,message,name):
        if name=="/bword":
            if getIsAdmin(self.bot,message):
                word = message.text
                if "/bword@szBrokenBot" in word:
                    word = word[word.index("/bword@szBrokenBot") + len("/bword@szBrokenBot"):]
                else:
                    word = word[word.index("/bword") + len("/bword"):]
                if len(word) == 0:
                    self.bot.reply_to(message, "Please type the word\n/bword word")
                else:
                    word = word.replace(" ","")
                    self.ban_word(message,word.lower())
            else:
                self.bot.reply_to(message,NOTADMIN)
        elif name=="/listbword":
            words = self.getBannedWordsByGroup(message.chat.id)
            if isinstance(words, str):
                self.bot.reply_to(message,"Ops, something went wonrg,retry!")
            else:
                if len(words)>0:
                    msgtosend=f"<b>Here is list of banned words:</b>\n"
                    for word in words:
                        msgtosend+=f"{word._word}\n"
                    self.bot.reply_to(message,msgtosend)
                else:
                    self.bot.reply_to(message, "This group has no banned words")
        elif name == "/dbword" :
            if getIsAdmin(self.bot,message):
                word = message.text
                if "/dbword@szBrokenBot" in word:
                    word = word[word.index("/dbword@szBrokenBot") + len("/dbword@szBrokenBot"):]
                else:
                    word = word[word.index("/dbword") + len("/dbword"):]
                if len(word) == 0:
                    self.bot.reply_to(message, "Please type the word\n/dbword word")
                else:
                    word = word.replace(" ", "")
                    self.rm_ban_word(message, word.lower())
            else:
                self.bot.reply_to(message, NOTADMIN)
    def ban_word(self, message, word):
        bannedword=BannedWords(message.id,message.chat.id,word,None)
        resp = self.insert_ban_word(bannedword)
        if resp=="ok":
            self.bot.reply_to(message, "Word added to banned list!")
        else:
            self.bot.reply_to(message,resp)
    def rm_ban_word(self, message, word):

        bannedword= BannedWords(message.id,message.chat.id,word,None)
        resp = self.deleteBannedWord(bannedword)

        self.bot.send_message(message.chat.id,resp)

    def insert_ban_word(self,bannedword):
        try:
            self.cursor.execute(f"""Select id from bannedwords where word='{bannedword._word}' AND groupid={bannedword._groupid}""")
            item = self.cursor.fetchall();
            if len(item)==0:
                self.cursor.execute(f"INSERT INTO bannedwords VALUES ({bannedword._id},'{bannedword._word}','{bannedword._created_At}',{bannedword._groupid})")

            return "ok"
        except Exception:
            return "Something went wrong retry!"
    def getBannedWordsArrayByGroup(self,id):
        try:
            self.cursor.execute(f"""Select * from bannedwords where groupid={id}""")
            items =  self.cursor.fetchall()
            arrayI = []
            for i in items:
                arrayI.append(i[1])

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    def getBannedWordsByGroup(self,id):
        try:
            self.cursor.execute(f"""Select * from bannedwords where groupid={id}""")
            items =  self.cursor.fetchall()
            arrayI = []
            for i in items:
                x = BannedWords(i[0],i[3],i[1],i[2])
                arrayI.append(x)

            return arrayI
        except Exception:
            return "Something went wrong retry!"
    # def getBannedWordsByGroup(self,id):
    #     try:
    #         self.cursor.execute(f"""Select * from bannedwords where groupid={id}""")
    #         items =  self.cursor.fetchall()
    #         arrayI = []
    #         for i in items:
    #             x = BannedWords(i[0],i[1],i[2],i[3])
    #             arrayI.append(x)
    #
    #         return arrayI
    #     except Exception:
    #         return "Something went wrong retry!"
    def deleteBannedWord(self,bannedword):

        try:
             self.cursor.execute(f"""DELETE FROM bannedwords
                                    WHERE word='{bannedword._word}'AND groupid={bannedword._groupid}""")
             count = self.cursor.rowcount
             if count>0:
                 return "Word deleted!"
             else:
                return "Word not found"
        except Exception:
            return "Something went wrong retry!"



    def getEveryMessageMethod(self,message):
        words = self.getBannedWordsArrayByGroup(message.chat.id)
        if len(words)>0:
            try:
                for word in words:
                    if word.lower() in message.text.lower():

                        self.bot.delete_message(message.chat.id,message.id)
            except:
                pass
